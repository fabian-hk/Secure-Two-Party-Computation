from typing import Dict
from protobuf import FunctionIndependentPreprocessing_pb2, FunctionDependentPreprocessing_pb2
from tools import fpre
from tools.person import Person
from gate import *


class MPC_B:

    def __init__(self, person: Person):
        # holds all gates like {int_id : gate}
        self.circuit: Dict[int, Gate] = {}

        # data structure to save the variables from the function independent preprocessing
        self.auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()

        self.person = person
        self.create_example_circuit()
        self.function_independent_preprocessing()

    def create_example_circuit(self):
        and0 = AND(10, self.person, None, None)
        self.circuit[1] = and0
        and1 = AND(20, self.person, None, None)
        self.circuit[2] = and1
        xor3 = XOR(30, self.person, and0, and1)
        self.circuit[3] = xor3

    def function_independent_preprocessing(self):
        self.person.delta = fpre.init_b()
        print(self.person)

        ser_auth_bits = fpre.rec_auth_bits()

        self.auth_bits.ParseFromString(ser_auth_bits)
        for auth_bit in self.auth_bits.bits:
            print("r: "+str(auth_bit.r))
            print("M: "+str(auth_bit.M))
            print("K: "+str(auth_bit.K))

    def function_dependent_preprocessing(self):
        ser_gates = FunctionDependentPreprocessing_pb2.GatesPreprocessing()
        for id in self.circuit.keys():
            ser_gate = ser_gates.gates.add()
            g = self.circuit[id]
            if g.type == Gate.TYPE_XOR:
                m0, m1 = fpre.create_gate_vars()
                ser_gate.M0 = m0
                ser_gate.M1 = m1
            elif g.type == Gate.TYPE_AND:
                g.function_dependent_preprocessing(ser_gates.gates.add())


if __name__ == "__main__":
    person = Person(Person.B)
    mpc = MPC_B(person)
