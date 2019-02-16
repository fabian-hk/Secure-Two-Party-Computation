from typing import Dict
from protobuf import FunctionIndependentPreprocessing_pb2, FunctionDependentPreprocessing_pb2
from tools import fpre
from tools.person import Person
from gate import *
import os
import conf


class MPC_A:

    def __init__(self, person: Person):
        # holds all gates like {int_id : gate}
        self.circuit: Dict[int, Gate] = {}

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

        auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBit()
        for id in self.circuit.keys():
            g = self.circuit[id]
            if g.type == Gate.TYPE_XOR and not g.pre_a and not g.pre_b:
                auth_bit = auth_bits.bits.add()
                auth_bit.id = id
                g.a, g.Ma, g.Ka = fpre.authenticated_bit(auth_bit)
                auth_bit = auth_bits.bits.add()
                auth_bit.id = id + 1
                g.b, g.Mb, g.Kb = fpre.authenticated_bit(auth_bit)
            elif g.type == Gate.TYPE_AND:
                # choose labels
                g.La0 = os.urandom(conf.k)
                g.Lb0 = os.urandom(conf.k)
                g.Ly0 = os.urandom(conf.k)
                # create authenticated bits
                auth_bit = auth_bits.bits.add()
                auth_bit.id = id+2
                g.y, g.My, g.Ky = fpre.authenticated_bit(auth_bit)

                # create authenticated bits if the gate is an input gate
                if not g.pre_a and not g.pre_b:
                    auth_bit = auth_bits.bits.add()
                    auth_bit.id = id
                    g.a, g.Ma, g.Ka = fpre.authenticated_bit(auth_bit)
                    auth_bit = auth_bits.bits.add()
                    auth_bit.id = id + 1
                    g.b, g.Mb, g.Kb = fpre.authenticated_bit(auth_bit)

        # Serialize the authenticated bits to the server
        fpre.send_auth_bits(auth_bits.SerializeToString())

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
