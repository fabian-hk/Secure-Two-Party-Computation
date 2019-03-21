from typing import Dict
from protobuf import FunctionIndependentPreprocessing_pb2, FunctionDependentPreprocessing_pb2, Wrapper
from tools import fpre
from tools.person import Person
import tools.helper as h
from tools.communication import Com
from gate import *
import os
import conf


class MPC:

    def __init__(self, person: Person):
        # holds all gates like {int_id : gate}
        self.circuit: Dict[int, Gate] = {}  # TODO delete variable

        self.person = person

        # data structures to store the variables from the function independent preprocessing
        if self.person.x == Person.A: self.labels = []
        self.auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()

        self.inputs = []
        self.outputs = []

        self.create_example_circuit()
        self.function_independent_preprocessing()
        self.function_dependent_preprocessing()

    def create_example_circuit(self):
        and0 = AND(10, self.person, None, None)
        self.circuit[10] = and0
        and1 = AND(20, self.person, None, None)
        self.circuit[20] = and1
        xor3 = XOR(30, self.person, and0, and1)
        self.circuit[30] = xor3
        self.inputs = [and0, and1]
        self.outputs.append(xor3)

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
        garbled_gates = FunctionDependentPreprocessing_pb2.GarbledGates()
        label_iter = iter(self.labels) if self.person.x == Person.A else None
        for out in self.outputs:
            self.gate_initialization(out, garbled_gates, label_iter)

        for key in self.circuit.keys():
            print(self.circuit[key])

    def gate_initialization(self, gate, garbled_gates, label_iter):
        """
        :param gate:
        :type gate Gate
        :param garbled_gates
        """
        if not gate.La0 and gate.pre_a:
            self.gate_initialization(gate.pre_a, garbled_gates, label_iter)
        if not gate.Lb0 and gate.pre_b:
            self.gate_initialization(gate.pre_b, garbled_gates, label_iter)
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
                gate.function_dependent_preprocessing(garbled_gates.gates.add())

                # as A send and triple to the fpre server
                if self.person.x == Person.A: fpre.and_triples(and_triple.SerializeToString())

                # propagate variables to the successor gates
                for n in gate.next:  # type: tuple[Gate, int]
                    if n[1] == Gate.WIRE_A:
                        if self.person.x == Person.A: n[0].La0 = label_iter.__next__()
                        n[0].a = gate.yi[0]
                        n[0].Ma = gate.Myi[0]
                        n[0].Ka = gate.Kyi[0]
                    else:
                        if self.person.x == Person.A: n[0].Lb0 = label_iter.__next__()
                        n[0].b = gate.yi[0]
                        n[0].Mb = gate.Myi[0]
                        n[0].Kb = gate.Kyi[0]

    def key_by_wire_id(self, id):
        for in_g in self.inputs:  # type: Gate
            if in_g.id == (id - (id % 10)):
                if id % 10 == 0:
                    return in_g.Ka
                if id % 10 == 1:
                    return in_g.Kb
        return None

    def input_preprocessing(self, in_vals: Dict[int, int]):
        """
        :param in_vals: Keys are the IDs of the input wires and values are the input bits
        """
        in_auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
        for in_gate in self.inputs:  # type: Gate
            if in_gate.id in in_vals:
                b = in_auth_bits.bits.add()
                b.id = in_gate.id
                b.r = in_gate.a
                b.M = in_gate.Ma
            if (in_gate.id + 1) in in_vals:
                b = in_auth_bits.bits.add()
                b.id = in_gate.id + 1
                b.r = in_gate.b
                b.M = in_gate.Mb

        com = Com(self.person)
        rec_auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
        rec_auth_bits.ParseFromString(com.exchange_data(0, in_auth_bits.SerializeToString()))

        # check tags
        print("------------- received -----------------")
        print(rec_auth_bits)
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

