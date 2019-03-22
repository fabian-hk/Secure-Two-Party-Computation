from typing import Dict
from protobuf import FunctionIndependentPreprocessing_pb2, FunctionDependentPreprocessing_pb2
from tools import fpre
from tools.person import Person
from MPC import MPC
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
        self.function_dependent_preprocessing()

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
        and_triples = FunctionDependentPreprocessing_pb2.ANDTriples()
        auth_bits = iter(self.auth_bits.bits)
        for id in self.circuit.keys():
            g = self.circuit[id]
            if g.type == Gate.TYPE_AND:
                and_triple = and_triples.triples.add()
                and_triple.id = id
                auth_bit = auth_bits.__next__()
                and_triple.r1 = auth_bit.r
                and_triple.M1 = auth_bit.M
                and_triple.K1 = auth_bit.K
                auth_bit = auth_bits.__next__()
                and_triple.r2 = auth_bit.r
                and_triple.M2 = auth_bit.M
                and_triple.K2 = auth_bit.K
                auth_bit = auth_bits.__next__()
                and_triple.r3 = auth_bit.r
                and_triple.M3 = auth_bit.M
                and_triple.K3 = auth_bit.K
        fpre.and_triples(and_triples.SerializeToString())
        print(and_triples)


if __name__ == "__main__":
    person = Person(Person.A)
    mpc = MPC(person)
    in_vals = {10: 0, 20: 1}
    other_in = [11, 21]
    mpc.input_processing(in_vals, other_in)
