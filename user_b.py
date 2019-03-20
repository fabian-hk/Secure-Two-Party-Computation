from typing import Dict
from protobuf import FunctionIndependentPreprocessing_pb2, FunctionDependentPreprocessing_pb2, Wrapper
from tools import fpre
from tools.person import Person
from gate import *


class MPC_B:

    def __init__(self, person: Person):
        # holds all gates like {int_id : gate}
        self.circuit: Dict[int, Gate] = {}

        # data structure to save the variables from the function independent preprocessing
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
        self.person.delta = fpre.init_b()

        self.auth_bits.ParseFromString(fpre.rec_auth_bits())

    def function_dependent_preprocessing(self):
        garbled_gates = FunctionDependentPreprocessing_pb2.GarbledGates()
        for out in self.outputs:
            self.gate_initialization(out, garbled_gates)

        for key in self.circuit.keys():
            print(self.circuit[key])

    def gate_initialization(self, gate, garbled_gates):
        """
        :param gate:
        :type gate Gate
        :param garbled_gates
        """
        if not gate.La0 and gate.pre_a:
            self.gate_initialization(gate.pre_a, garbled_gates)
        if not gate.Lb0 and gate.pre_b:
            self.gate_initialization(gate.pre_b, garbled_gates)
        if not gate.prepro:
            gate.prepro = True
            if gate.type == Gate.TYPE_XOR:
                if not gate.pre_a:
                    gate.initialize_vars(auth_bit_A=Wrapper.get_auth_bit_by_id(gate.id, self.auth_bits))
                if not gate.pre_b:
                    gate.initialize_vars(auth_bit_B=Wrapper.get_auth_bit_by_id(gate.id + 1, self.auth_bits))
                gate.function_dependent_preprocessing()
                for n in gate.next:  # type: tuple[Gate, int]
                    if n[1] == Gate.WIRE_A:
                        n[0].a = gate.y
                        n[0].Ma = gate.My
                        n[0].Ka = gate.Ky
                    else:
                        n[0].b = gate.y
                        n[0].Mb = gate.My
                        n[0].Kb = gate.Ky
            elif gate.type == Gate.TYPE_AND:
                and_triple = FunctionDependentPreprocessing_pb2.ANDTriple()
                and_triple.id = gate.id
                if not gate.pre_a:
                    gate.initialize_vars(auth_bit_A=Wrapper.get_auth_bit_by_id(gate.id, self.auth_bits),
                                         and_triple=and_triple)
                else:
                    gate.get_auth_bit(and_triple, Gate.WIRE_A)
                if not gate.pre_b:
                    gate.initialize_vars(auth_bit_B=Wrapper.get_auth_bit_by_id(gate.id + 1, self.auth_bits),
                                         and_triple=and_triple)
                else:
                    gate.get_auth_bit(and_triple, Gate.WIRE_B)

                and_triple.ParseFromString(fpre.and_triples(and_triple.SerializeToString()))

                gate.initialize_auth_bit_o(and_triple, self.person)
                gate.initialize_auth_bit_y(Wrapper.get_auth_bit_by_id(gate.id + 2, self.auth_bits))

                gate.function_dependent_preprocessing()

                for n in gate.next:  # type: tuple[Gate, int]
                    if n[1] == Gate.WIRE_A:
                        n[0].a = gate.yi[0]
                        n[0].Ma = gate.Myi[0]
                        n[0].Ka = gate.Kyi[0]
                    else:
                        n[0].b = gate.yi[0]
                        n[0].Mb = gate.Myi[0]
                        n[0].Kb = gate.Kyi[0]


if __name__ == "__main__":
    person = Person(Person.B)
    mpc = MPC_B(person)
