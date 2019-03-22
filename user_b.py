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
        self.function_dependent_preprocessing()

    def create_example_circuit(self):
        and0 = AND(10, self.person, None, None)
        self.circuit[10] = and0
        and1 = AND(20, self.person, None, None)
        self.circuit[20] = and1
        xor3 = XOR(30, self.person, and0, and1)
        self.circuit[30] = xor3

    def function_independent_preprocessing(self):
        self.person.delta = fpre.init_b()

        ser_auth_bits = fpre.rec_auth_bits()

        self.auth_bits.ParseFromString(ser_auth_bits)

    def function_dependent_preprocessing(self):
        and_triples_tmp = FunctionDependentPreprocessing_pb2.ANDTriples()
        auth_bits = iter(self.auth_bits.bits)
        for id in self.circuit.keys():
            g = self.circuit[id]
            if g.type == Gate.TYPE_AND:
                and_triple = and_triples_tmp.triples.add()
                and_triple.id = id
                auth_bit = auth_bits.__next__()
                and_triple.r1 = auth_bit.r
                and_triple.M1 = auth_bit.M
                and_triple.K1 = auth_bit.K
                auth_bit = auth_bits.__next__()
                and_triple.r2 = auth_bit.r
                and_triple.M2 = auth_bit.M
                and_triple.K2 = auth_bit.K
        and_triples = FunctionDependentPreprocessing_pb2.ANDTriples()
        and_triples.ParseFromString(fpre.and_triples(and_triples_tmp.SerializeToString()))
        print(and_triples)


if __name__ == "__main__":
    person = Person(Person.B)
    mpc = MPC_B(person)
