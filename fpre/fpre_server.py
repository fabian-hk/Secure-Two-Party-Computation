import os
import sys
from random import randint

import conf
import tools.helper as h
from protobuf import FunctionIndependentPreprocessing_pb2, FunctionDependentPreprocessing_pb2


class FpreServer:

    def __init__(self):
        self.delta_a = None
        self.delta_b = None

    def init(self, data_A):
        self.delta_a = data_A
        self.delta_b = os.urandom(int(conf.k / 8))
        return self.delta_b

    def create_auth_bits(self, data_A):
        auth_bits_A = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
        auth_bits_B = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
        try:
            auth_bits_A.ParseFromString(data_A)
        except:
            print("parse auth bits a: " + str(data_A))
        for auth_bit_A in auth_bits_A.bits:
            auth_bit_B = auth_bits_B.bits.add()
            auth_bit_B.id = auth_bit_A.id
            r = randint(0, 1)  # TODO change to os.urandom for safety??
            auth_bit_B.r = r.to_bytes(1, 'big')

            if auth_bit_A.r == b'\x00':
                auth_bit_B.K = auth_bit_A.M
            else:
                auth_bit_B.K = bytes(h.xor(auth_bit_A.M, self.delta_b))

            if auth_bit_B.r == b'\x00':
                auth_bit_B.M = auth_bit_A.K
            else:
                auth_bit_B.M = bytes(h.xor(auth_bit_A.K, self.delta_a))

        return auth_bits_B.SerializeToString()

    def create_and_triple(self, data_A, data_B):
        and_triple_A = FunctionDependentPreprocessing_pb2.ANDTriple()
        and_triple_A.ParseFromString(data_A)
        and_triple_B = FunctionDependentPreprocessing_pb2.ANDTriple()
        and_triple_B.ParseFromString(data_B)

        if and_triple_A.id != and_triple_B.id:
            print("Error IDs not equal!")
            sys.exit(1)

        # check AND triple
        h.check_and_triple(and_triple_A, and_triple_B, self.delta_a, self.delta_b)

        and_triple_B.r3 = bytes(h.xor(and_triple_A.r3, h.AND(h.xor(and_triple_A.r1, and_triple_B.r1),
                                                             h.xor(and_triple_A.r2, and_triple_B.r2))))
        if and_triple_B.r3 == b'\x01':
            and_triple_B.M3 = bytes(h.xor(and_triple_A.K3, self.delta_a))
        else:
            and_triple_B.M3 = and_triple_A.K3
        if and_triple_A.r3 == b'\x01':
            and_triple_B.K3 = bytes(h.xor(and_triple_A.M3, self.delta_b))
        else:
            and_triple_B.K3 = and_triple_A.M3

        """
        if and_triple_B.r3 == b'\x01':
            if and_triple_B.M3 == h.xor(and_triple_A.K3, delta_a):
                print("Correct. AND triple ID: "+str(and_triple_B.id))
            else:
                print(and_triple_A)
                print(and_triple_B)
                print("Cheat. AND triple ID: "+str(and_triple_B.id))
        else:
            if and_triple_B.M3 == and_triple_A.K3:
                print("Correct. AND triple ID: " + str(and_triple_B.id))
            else:
                print(and_triple_A)
                print(and_triple_B)
                print("Cheat. AND triple ID: " + str(and_triple_B.id))
        """
        return and_triple_B.SerializeToString()
