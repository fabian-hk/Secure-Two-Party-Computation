from typing import Dict
from protobuf import FunctionIndependentPreprocessing_pb2, FunctionDependentPreprocessing_pb2, Wrapper
from tools import fpre
from tools.person import Person
from gate import *
import os
import conf
import math


class MPC_A:

    def __init__(self, person: Person):
        # holds all gates like {int_id : gate}
        self.circuit: Dict[int, Gate] = {}

        # data structures to store the variables from the function independent preprocessing
        self.labels = []
        self.auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()

        self.outputs = []

        self.person = person
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
        self.outputs.append(xor3)

    def function_independent_preprocessing(self):
        fpre.init_a(self.person)
        print(person)

        for i in range(conf.upper_bound_gates):
            for j in range(3):
                auth_bit = self.auth_bits.bits.add()
                auth_bit.id = i * 10 + j
                fpre.authenticated_bit(auth_bit)
                self.labels.append(os.urandom(int(conf.k / 8)))

        # Serialize the authenticated bits and send them to the server
        fpre.send_auth_bits(self.auth_bits.SerializeToString())

    def function_dependent_preprocessing(self):
        garbled_gates = FunctionDependentPreprocessing_pb2.GarbledGates()
        label_iter = iter(self.labels)
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
                    gate.La0 = label_iter.__next__()
                if not gate.pre_b:
                    gate.initialize_vars(auth_bit_B=Wrapper.get_auth_bit_by_id(gate.id + 1, self.auth_bits))
                    gate.Lb0 = label_iter.__next__()

                # do the function dependent preprocessing
                gate.function_dependent_preprocessing()

                # propagate variables to the successor gates
                for n in gate.next:  # type: tuple[Gate, int]
                    if n[1] == Gate.WIRE_A:
                        n[0].La0 = gate.Ly0
                        n[0].a = gate.y
                        n[0].Ma = gate.My
                        n[0].Ka = gate.Ky
                    else:
                        n[0].Lb0 = gate.Ly0
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
                    gate.La0 = label_iter.__next__()
                else:
                    gate.get_auth_bit(and_triple, Gate.WIRE_A)
                if not gate.pre_b:
                    gate.initialize_vars(auth_bit_B=Wrapper.get_auth_bit_by_id(gate.id + 1, self.auth_bits),
                                         and_triple=and_triple)
                    gate.Lb0 = label_iter.__next__()
                else:
                    gate.get_auth_bit(and_triple, Gate.WIRE_B)

                gate.Ly0 = label_iter.__next__()

                gate.initialize_auth_bit_o(and_triple, self.person)
                gate.initialize_auth_bit_y(Wrapper.get_auth_bit_by_id(gate.id + 2, self.auth_bits))

                # do the function dependent preprocessing
                gate.function_dependent_preprocessing(garbled_gates.gates.add())

                # send and triple to the fpre server
                fpre.and_triples(and_triple.SerializeToString())

                # propagate variables to the successor gates
                for n in gate.next:  # type: tuple[Gate, int]
                    if n[1] == Gate.WIRE_A:
                        n[0].La0 = label_iter.__next__()
                        n[0].a = gate.yi[0]
                        n[0].Ma = gate.Myi[0]
                        n[0].Ka = gate.Kyi[0]
                    else:
                        n[0].Lb0 = label_iter.__next__()
                        n[0].b = gate.yi[0]
                        n[0].Mb = gate.Myi[0]
                        n[0].Kb = gate.Kyi[0]


if __name__ == "__main__":
    person = Person(Person.A)
    mpc = MPC_A(person)
