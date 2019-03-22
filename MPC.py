from typing import Dict, List
import os

from protobuf import FunctionIndependentPreprocessing_pb2, FunctionDependentPreprocessing_pb2, InputPreprocessing_pb2, \
    Wrapper
from tools.communication import Com
from tools.gate import *

import conf


class MPC:

    def __init__(self, person: Person):
        self.person = person

        # data structures to store the variables from the function independent preprocessing
        if self.person.x == Person.A: self.labels = []
        self.auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()

        self.inputs = None
        self.outputs = None
        self.garbled_gates = FunctionDependentPreprocessing_pb2.GarbledGates()

        self.com = None

        self.in_bits = InputPreprocessing_pb2.Inputs()
        self.rec_in_bits = InputPreprocessing_pb2.Inputs()

        self.function_independent_preprocessing()

    def load_cirucit(self, inputs: List, outputs: List):
        """
        Loads the list with the input and output gates of the cirucit.
        :param inputs:
        :param outputs:
        """
        self.inputs = inputs
        self.outputs = outputs

    def function_independent_preprocessing(self):
        if self.person.x == Person.A:
            fpre.init_a(self.person)
            for i in range(conf.upper_bound_gates):
                for j in range(3):
                    auth_bit = self.auth_bits.bits.add()
                    auth_bit.id = i * 10 + j
                    fpre.authenticated_bit(auth_bit)
                    self.labels.append(os.urandom(int(conf.k / 8)))

            # Serialize the authenticated bits and send them to the server
            fpre.send_auth_bits(self.auth_bits.SerializeToString())
        else:
            self.person.delta = fpre.init_b()
            self.auth_bits.ParseFromString(fpre.rec_auth_bits())

    def function_dependent_preprocessing(self):
        label_iter = iter(self.labels) if self.person.x == Person.A else None
        for out in self.outputs:
            self.gate_initialization(out, label_iter)

        fpre.close_session()

        self.com = Com(self.person)

        if self.person.x == Person.A:
            self.com.exchange_data(0, self.garbled_gates.SerializeToString())
        else:
            self.garbled_gates.ParseFromString(self.com.exchange_data(0))
        print(self.garbled_gates)

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
                    gate.initialize_vars(auth_bit_A=Wrapper.get_auth_bit_by_id(gate.id, self.auth_bits))
                    if self.person.x == Person.A: gate.La0 = label_iter.__next__()
                if not gate.pre_b:
                    gate.initialize_vars(auth_bit_B=Wrapper.get_auth_bit_by_id(gate.id + 1, self.auth_bits))
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
                    gate.initialize_vars(auth_bit_A=Wrapper.get_auth_bit_by_id(gate.id, self.auth_bits),
                                         and_triple=and_triple)
                    if self.person.x == Person.A: gate.La0 = label_iter.__next__()
                else:
                    gate.get_auth_bit(and_triple, Gate.WIRE_A)
                if not gate.pre_b:
                    gate.initialize_vars(auth_bit_B=Wrapper.get_auth_bit_by_id(gate.id + 1, self.auth_bits),
                                         and_triple=and_triple)
                    if self.person.x == Person.A: gate.Lb0 = label_iter.__next__()
                else:
                    gate.get_auth_bit(and_triple, Gate.WIRE_B)

                if self.person.x == Person.A: gate.Ly0 = label_iter.__next__()

                # as B send the and double to the fpre server to receive the missing bit
                if self.person.x == Person.B: and_triple.ParseFromString(
                    fpre.and_triples(and_triple.SerializeToString()))

                gate.initialize_auth_bit_o(and_triple, self.person)
                gate.initialize_auth_bit_y(Wrapper.get_auth_bit_by_id(gate.id + 2, self.auth_bits))

                # do the function dependent preprocessing
                gate.function_dependent_preprocessing(self.garbled_gates.gates.add())

                # as A send and triple to the fpre server
                if self.person.x == Person.A: fpre.and_triples(and_triple.SerializeToString())

                # propagate variables to the successor gates
                for n in gate.next:  # type: tuple[Gate, int]
                    if n[1] == Gate.WIRE_A:
                        if self.person.x == Person.A: n[0].La0 = label_iter.__next__()
                        n[0].a = gate.y
                        n[0].Ma = gate.My
                        n[0].Ka = gate.Ky
                    else:
                        if self.person.x == Person.A: n[0].Lb0 = label_iter.__next__()
                        n[0].b = gate.y
                        n[0].Mb = gate.My
                        n[0].Kb = gate.Ky

    def key_by_wire_id(self, id: int) -> bytes:
        for in_g in self.inputs:  # type: Gate
            if in_g.id == (id - (id % 10)):
                if id % 10 == 0:
                    return in_g.Ka
                if id % 10 == 1:
                    return in_g.Kb
        return None

    def label_by_wire_id(self, id: int, l: bytes) -> bytes:
        for in_g in self.inputs:  # type: Gate
            if in_g.id == (id - (id % 10)):
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

    def input_processing(self, in_vals: Dict[int, int], other_in: List[int]):
        """
        :param other_in:
        :param in_vals: Keys are the IDs of the input wires and values are the input bits
        """

        # assemble all input bits together either to send them over or to compute the masked bits
        # bits to send to the other party
        in_auth_bits_o = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
        # own input bits
        in_auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
        for in_gate in self.inputs:  # type: Gate
            if in_gate.id in other_in:
                b = in_auth_bits_o.bits.add()
                b.id = in_gate.id
                b.r = in_gate.a
                b.M = in_gate.Ma
            elif in_gate.id in in_vals:
                b = in_auth_bits.bits.add()
                b.id = in_gate.id
                b.r = in_gate.a
                b.M = in_gate.Ma

            if (in_gate.id + 1) in other_in:
                b = in_auth_bits_o.bits.add()
                b.id = in_gate.id + 1
                b.r = in_gate.b
                b.M = in_gate.Mb
            elif (in_gate.id + 1) in in_vals:
                b = in_auth_bits.bits.add()
                b.id = in_gate.id + 1
                b.r = in_gate.b
                b.M = in_gate.Mb

        rec_auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
        rec_auth_bits.ParseFromString(self.com.exchange_data(1, in_auth_bits_o.SerializeToString()))

        # check tags
        print("------------- Input bits check -----------------")
        for bit in rec_auth_bits.bits:
            key = self.key_by_wire_id(bit.id)
            if bit.r == b'\x01':
                if bit.M == bytes(h.xor(key, self.person.delta)):
                    print("Correct. ID: " + str(bit.id))
                else:
                    print("Cheat. ID: " + str(bit.id))
            else:
                if bit.M == key:
                    print("Correct. ID: " + str(bit.id))
                else:
                    print("Cheat. ID: " + str(bit.id))

        # compute the masked bit and A also computes directly the labels
        for in_auth_bit in in_auth_bits.bits:
            in_bit = self.in_bits.inputs.add()
            in_bit.id = in_auth_bit.id
            in_bit.masked_input = bytes(h.xor(in_auth_bit.r, in_vals[in_bit.id].to_bytes(1, 'big'),
                                              Wrapper.get_auth_bit_by_id(in_bit.id, rec_auth_bits).r))
            if self.person.x == Person.A: in_bit.label = bytes(self.label_by_wire_id(in_bit.id, in_bit.masked_input))

        # exchange bits
        self.rec_in_bits.ParseFromString(self.com.exchange_data(2, self.in_bits.SerializeToString()))
        if self.person.x == Person.A:
            # A assembles all labels for B with the masked bits from B
            for rec_in_bit in self.rec_in_bits.inputs:
                rec_in_bit.label = bytes(self.label_by_wire_id(rec_in_bit.id, rec_in_bit.masked_input))
            self.com.exchange_data(3, self.rec_in_bits.SerializeToString())
        # B receives the labels for his input from A
        if self.person.x == Person.B: self.in_bits.ParseFromString(self.com.exchange_data(3))

        print("----------- in bits --------------")
        print(self.in_bits)
        print("----------- rec in bits --------------")
        print(self.rec_in_bits)

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
            print(out)

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

    def output_determination(self):
        print("------------------ output determination ---------------------")
        auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
        if self.person.x == Person.A:
            for out in self.outputs:  # type: Gate
                out.get_y_auth_bit(auth_bits.bits.add())
            self.com.exchange_data(5, auth_bits.SerializeToString())
        else:
            auth_bits.ParseFromString(self.com.exchange_data(5))
            for out in self.outputs:  # type: Gate
                auth_bit = Wrapper.get_auth_bit_by_id(out.id, auth_bits)
                if auth_bit.r == b'\x01':
                    if auth_bit.M == h.xor(out.Ky, self.person.delta):
                        print("Correct. ID: " + str(out.id))
                    else:
                        print("Cheat. ID: " + str(out.id))
                else:
                    if auth_bit.M == out.Ky:
                        print("Correct. ID: " + str(out.id))
                    else:
                        print("Cheat. ID: " + str(out.id))

                res = h.xor(out.masked_bit_y, auth_bit.r, out.y)
                print("Result bit " + str(out.id) + ": " + str(res))
