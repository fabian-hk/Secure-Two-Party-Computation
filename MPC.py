from typing import Dict, List
import os

from protobuf import FunctionIndependentPreprocessing_pb2, FunctionDependentPreprocessing_pb2, InputPreprocessing_pb2, \
    Output_pb2, Wrapper
from tools.gate import *
from fpre.fpre import Fpre
import fpre.f_a_and as faand
import conf
from exceptions.CheaterException import CheaterRecognized


class MPC:

    def __init__(self, com: Fpre):
        self.com = com
        self.person = self.com.person

        # data structures to store the variables from the function independent preprocessing
        if self.person.x == Person.A: self.labels = []
        self.auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
        self.and_triples = None

        self.inputs = None
        self.outputs = None
        self.num_and = None
        self.garbled_gates = FunctionDependentPreprocessing_pb2.GarbledGates()

        self.in_bits = InputPreprocessing_pb2.Inputs()
        self.rec_in_bits = InputPreprocessing_pb2.Inputs()

        self.function_independent_preprocessing()

    def load_cirucit(self, inputs: Dict[int, Gate], outputs: List, num_and):
        """
        Loads the list with the input and output gates of the cirucit.
        :param num_and: number of and gates in the circuit
        :param inputs:
        :param outputs:
        """
        self.inputs = inputs
        self.outputs = outputs
        self.num_and = num_and

    def function_independent_preprocessing(self):
        self.com.init_fpre()
        if self.person.x == Person.A:
            for i in range(conf.upper_bound_gates):
                for j in range(3):
                    auth_bit = self.auth_bits.bits.add()
                    auth_bit.id = i * 10 + j
                    self.com.authenticated_bit(auth_bit)
                    self.labels.append(os.urandom(int(conf.k / 8)))

            # Serialize the authenticated bits and send them to the server
            self.com.send_auth_bits(self.auth_bits.SerializeToString())
        else:
            self.auth_bits.ParseFromString(self.com.rec_auth_bits())

        # create iterator over auth_bits
        self.auth_bits = iter(self.auth_bits.bits)

    def function_dependent_preprocessing(self):
        label_iter = iter(self.labels) if self.person.x == Person.A else None
        self.and_triples = iter(faand.f_a_and(self.person, self.com, self.num_and).triples)
        for out in self.outputs:
            self.gate_initialization(out, label_iter)

        if self.person.x == Person.A:
            self.com.exchange_data(self.garbled_gates.SerializeToString())
        else:
            self.garbled_gates.ParseFromString(self.com.exchange_data())

    def gate_initialization(self, gate, label_iter):
        """
        :param gate:
        :type gate Gate
        :param garbled_gates
        """
        if not gate.a and gate.pre_a:
            self.gate_initialization(gate.pre_a, label_iter)
        if not gate.b and gate.pre_b:
            self.gate_initialization(gate.pre_b, label_iter)
        if not gate.prepro:
            gate.prepro = True
            if gate.type == Gate.TYPE_XOR:
                # initialize variables if they are not already initialized
                if not gate.pre_a:
                    gate.initialize_vars(auth_bit_A=next(self.auth_bits))
                    if self.person.x == Person.A: gate.La0 = label_iter.__next__()
                if not gate.pre_b:
                    gate.initialize_vars(auth_bit_B=next(self.auth_bits))
                    if self.person.x == Person.A: gate.Lb0 = label_iter.__next__()

                # do the function dependent preprocessing
                gate.function_dependent_preprocessing()

                # propagate variables to the successor gates
                for n in gate.next:  # type: tuple[Gate, int]
                    if n[1] == Gate.WIRE_A:
                        if self.person.x == Person.A: n[0].La0 = gate.Ly0
                        n[0].a = gate.y
                        n[0].Ma = gate.My
                        n[0].Ka = gate.Ky
                    else:
                        if self.person.x == Person.A: n[0].Lb0 = gate.Ly0
                        n[0].b = gate.y
                        n[0].Mb = gate.My
                        n[0].Kb = gate.Ky
            elif gate.type == Gate.TYPE_AND:
                and_triple = FunctionDependentPreprocessing_pb2.ANDTriple()
                and_triple.id = gate.id
                # initialize all variables and create the and triple
                if not gate.pre_a:
                    gate.initialize_vars(auth_bit_A=next(self.auth_bits),
                                         and_triple=and_triple)
                    if self.person.x == Person.A: gate.La0 = label_iter.__next__()
                else:
                    gate.get_auth_bit(and_triple, Gate.WIRE_A)
                if not gate.pre_b:
                    gate.initialize_vars(auth_bit_B=next(self.auth_bits),
                                         and_triple=and_triple)
                    if self.person.x == Person.A: gate.Lb0 = label_iter.__next__()
                else:
                    gate.get_auth_bit(and_triple, Gate.WIRE_B)

                if self.person.x == Person.A: gate.Ly0 = label_iter.__next__()

                # compute the complete AND triple
                faand.compute_and_triple(and_triple, next(self.and_triples), self.com, self.person)

                gate.initialize_auth_bit_o(and_triple)
                gate.initialize_auth_bit_y(next(self.auth_bits))

                # do the function dependent preprocessing
                gate.function_dependent_preprocessing(self.garbled_gates.gates.add())

                # propagate variables to the successor gates
                for n in gate.next:  # type: tuple[Gate, int]
                    if n[1] == Gate.WIRE_A:
                        if self.person.x == Person.A: n[0].La0 = gate.Ly0 if not gate.is_nand else h.xor(gate.Ly0,
                                                                                                         self.person.delta)
                        n[0].a = gate.y
                        n[0].Ma = gate.My
                        n[0].Ka = gate.Ky
                    else:
                        if self.person.x == Person.A: n[0].Lb0 = gate.Ly0 if not gate.is_nand else h.xor(gate.Ly0,
                                                                                                         self.person.delta)
                        n[0].b = gate.y
                        n[0].Mb = gate.My
                        n[0].Kb = gate.Ky

    def key_by_wire_id(self, id: int) -> bytes:
        in_g = self.inputs[(id - (id % 10))]  # type: Gate

        if id % 10 == 0:
            return in_g.Ka
        if id % 10 == 1:
            return in_g.Kb

        return None

    def label_by_wire_id(self, id: int, l: bytes) -> bytes:
        in_g = self.inputs[(id - (id % 10))]  # type: Gate

        if id % 10 == 0 and in_g.type == Gate.TYPE_AND and l == b'\x00':
            return in_g.La0
        elif id % 10 == 0 and in_g.type == Gate.TYPE_AND and l == b'\x01':
            return in_g.La1
        elif id % 10 == 1 and in_g.type == Gate.TYPE_AND and l == b'\x00':
            return in_g.Lb0
        elif id % 10 == 1 and in_g.type == Gate.TYPE_AND and l == b'\x01':
            return in_g.Lb1
        elif id % 10 == 0 and in_g.type == Gate.TYPE_XOR and l == b'\x00':
            return in_g.La0
        elif id % 10 == 0 and in_g.type == Gate.TYPE_XOR and l == b'\x01':
            return h.xor(in_g.La0, self.person.delta)
        elif id % 10 == 1 and in_g.type == Gate.TYPE_XOR and l == b'\x00':
            return in_g.Lb0
        elif id % 10 == 1 and in_g.type == Gate.TYPE_XOR and l == b'\x01':
            return h.xor(in_g.Lb0, self.person.delta)

        return None

    def input_processing(self):
        # assemble all input bits together either to send them over or to compute the masked bits
        # bits to send to the other party
        in_auth_bits_o = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
        # own input bits
        in_auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
        for in_gate in self.inputs.values():  # type: Gate
            if in_gate.id in self.person.other_inputs:
                b = in_auth_bits_o.bits.add()
                b.id = in_gate.id
                b.r = in_gate.a
                b.M = in_gate.Ma
            elif in_gate.id in self.person.inputs:
                b = in_auth_bits.bits.add()
                b.id = in_gate.id
                b.r = in_gate.a
                b.M = in_gate.Ma

            if (in_gate.id + 1) in self.person.other_inputs:
                b = in_auth_bits_o.bits.add()
                b.id = in_gate.id + 1
                b.r = in_gate.b
                b.M = in_gate.Mb
            elif (in_gate.id + 1) in self.person.inputs:
                b = in_auth_bits.bits.add()
                b.id = in_gate.id + 1
                b.r = in_gate.b
                b.M = in_gate.Mb

        rec_auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
        rec_auth_bits.ParseFromString(self.com.exchange_data(in_auth_bits_o.SerializeToString()))

        # check tags
        print("------------- Input bits check -----------------")
        for bit in rec_auth_bits.bits:
            key = self.key_by_wire_id(bit.id)
            if bit.r == b'\x01':
                if bit.M != bytes(h.xor(key, self.person.delta)):
                    raise CheaterRecognized()
            else:
                if bit.M != key:
                    raise CheaterRecognized()
        print("Auth bits verification passed")

        # compute the masked bit and A also computes directly the labels
        for in_auth_bit in in_auth_bits.bits:
            in_bit = self.in_bits.inputs.add()
            in_bit.id = in_auth_bit.id
            in_bit.masked_input = bytes(h.xor(in_auth_bit.r, self.person.in_vals[in_bit.id],
                                              Wrapper.get_auth_bit_by_id(in_bit.id, rec_auth_bits).r))
            if self.person.x == Person.A: in_bit.label = bytes(self.label_by_wire_id(in_bit.id, in_bit.masked_input))

        # exchange bits
        self.rec_in_bits.ParseFromString(self.com.exchange_data(self.in_bits.SerializeToString()))
        if self.person.x == Person.A:
            # A assembles all labels for B with the masked bits from B
            for rec_in_bit in self.rec_in_bits.inputs:
                rec_in_bit.label = bytes(self.label_by_wire_id(rec_in_bit.id, rec_in_bit.masked_input))
            self.com.exchange_data(self.rec_in_bits.SerializeToString())
        # B receives the labels for his input from A
        if self.person.x == Person.B: self.in_bits.ParseFromString(self.com.exchange_data())

    def get_inputs_by_id(self, id: int) -> (bytes, bytes):
        for bit in self.in_bits.inputs:
            if bit.id == id:
                return bit.masked_input, bit.label
        for bit in self.rec_in_bits.inputs:
            if bit.id == id:
                return bit.masked_input, bit.label
        return None

    def circuit_evaluation(self):
        print("--------------- evaluation -----------------")
        for out in self.outputs:
            self.circuit_evaluation_recursive(out)
        print("Auth bits verification passed")

    def circuit_evaluation_recursive(self, gate: Gate):
        if not gate.label_a and gate.pre_a:
            self.circuit_evaluation_recursive(gate.pre_a)
        if not gate.label_b and gate.pre_b:
            self.circuit_evaluation_recursive(gate.pre_b)
        if not gate.evaluated:
            gate.evaluated = True
            # if gate has inputs then retrieve the values from the input processing
            if not gate.label_a or not gate.masked_bit_a:
                gate.masked_bit_a, gate.label_a = self.get_inputs_by_id(gate.id)
            if not gate.label_b or not gate.masked_bit_b:
                gate.masked_bit_b, gate.label_b = self.get_inputs_by_id(gate.id + 1)

            gate.circuit_evaluation(Wrapper.get_garbled_gate_bit_by_id(gate.id, self.garbled_gates))

            for n in gate.next:  # type: tuple[Gate, int]
                if n[1] == Gate.WIRE_A:
                    n[0].masked_bit_a = gate.masked_bit_y
                    n[0].label_a = gate.label_y
                elif n[1] == Gate.WIRE_B:
                    n[0].masked_bit_b = gate.masked_bit_y
                    n[0].label_b = gate.label_y

    def output_determination(self) -> Dict[int, bytearray]:
        print("------------------ output determination ---------------------")
        auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
        outputs = Output_pb2.Outputs()
        if self.person.x == Person.A:
            for out in self.outputs:  # type: Gate
                out.get_y_auth_bit(auth_bits.bits.add())
            self.com.exchange_data(auth_bits.SerializeToString())
            outputs.ParseFromString(self.com.exchange_data())
            self.com.close_session()
            print()
            print(outputs)
        else:
            auth_bits.ParseFromString(self.com.exchange_data())
            auth_bits = iter(auth_bits.bits)
            result = {}
            for out in self.outputs:  # type: Gate
                auth_bit = next(auth_bits)
                if auth_bit.r == b'\x01':
                    if auth_bit.M != h.xor(out.Ky, self.person.delta):
                        raise CheaterRecognized()
                else:
                    if auth_bit.M != out.Ky:
                        raise CheaterRecognized()

                res = h.xor(out.masked_bit_y, auth_bit.r, out.y)
                result[out.id] = res
                output = outputs.outputs.add()
                output.id = out.id + 2
                output.output = bytes(res)
            print("Auth bits verification passed")

            self.com.exchange_data(outputs.SerializeToString())
            self.com.close_session()
            print()
            print(outputs)
            return result
