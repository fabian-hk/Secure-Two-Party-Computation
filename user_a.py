from typing import Dict
from protobuf import FunctionIndependentPreprocessing_pb2, FunctionDependentPreprocessing_pb2
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

        self.person = person
        self.create_example_circuit()
        self.function_independent_preprocessing()

    def create_example_circuit(self):
        and0 = AND(10, self.person, None, None)
        self.circuit[10] = and0
        and1 = AND(20, self.person, None, None)
        self.circuit[20] = and1
        xor3 = XOR(30, self.person, and0, and1)
        self.circuit[30] = xor3

    def function_independent_preprocessing(self):
        fpre.init_a(self.person)
        print(person)

        for i in range((conf.upper_bound_gates + 2 * conf.input_size)):
            auth_bit = self.auth_bits.bits.add()
            fpre.authenticated_bit(auth_bit)
            self.labels.append(os.urandom(int(conf.k / 8)))

        # Serialize the authenticated bits and send them to the server
        fpre.send_auth_bits(self.auth_bits.SerializeToString())

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
    person = Person(Person.A)
    mpc = MPC_A(person)
