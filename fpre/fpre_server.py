import socket
import os
import conf
import tools.helper as h
from random import randint
from protobuf import FunctionIndependentPreprocessing_pb2, FunctionDependentPreprocessing_pb2
from protobuf import Wrapper
import sys

TCP_IP = 'localhost'
TCP_PORT = 3003
BUFFER_SIZE = 2048

delta_a = None
delta_b = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)


def receive(conn):
    data = bytes(0)
    while True:
        part = conn.recv(BUFFER_SIZE)
        data += part
        if len(part) < BUFFER_SIZE:
            break
    return data


while True:
    print("Waiting for connection")

    conn1, addr1 = s.accept()
    print("First connection. IP: " + str(addr1))

    conn2, addr2 = s.accept()
    print("Second connection. IP: " + str(addr2))

    print()

    run = True
    while run:
        data_A = receive(conn1)
        if not data_A:
            continue
        if data_A[0] == 0:
            delta_a = data_A[1:]
            delta_b = os.urandom(int(conf.k / 8))
            conn2.send(b'\x00' + delta_b)
            conn1.send(b'\x00')
        elif data_A[0] == 1:
            auth_bits_A = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
            auth_bits_B = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
            auth_bits_A.ParseFromString(data_A[1:])
            for auth_bit_A in auth_bits_A.bits:
                auth_bit_B = auth_bits_B.bits.add()
                auth_bit_B.id = auth_bit_A.id
                r = randint(0, 1)  # TODO change to os.urandom for safety??
                auth_bit_B.r = r.to_bytes(1, 'big')

                if auth_bit_A.r == b'\x00':
                    auth_bit_B.K = auth_bit_A.M
                else:
                    auth_bit_B.K = bytes(h.xor(auth_bit_A.M, delta_b))

                if auth_bit_B.r == b'\x00':
                    auth_bit_B.M = auth_bit_A.K
                else:
                    auth_bit_B.M = bytes(h.xor(auth_bit_A.K, delta_a))

            ser_auth_bits = auth_bits_B.SerializeToString()
            conn2.send(b'\x01' + ser_auth_bits)
            conn1.send(b'\x01')
        elif data_A[0] == 2:
            and_triple_A = FunctionDependentPreprocessing_pb2.ANDTriple()
            and_triple_A.ParseFromString(data_A[1:])
            data_B = receive(conn2)
            and_triple_B = FunctionDependentPreprocessing_pb2.ANDTriple()
            and_triple_B.ParseFromString(data_B[1:])

            if and_triple_A.id != and_triple_B.id:
                print("Error IDs not equal!")
                sys.exit(1)

            # check AND triple
            h.check_and_triple(and_triple_A, and_triple_B, delta_a, delta_b)

            and_triple_B.r3 = bytes(h.xor(and_triple_A.r3, h.AND(h.xor(and_triple_A.r1, and_triple_B.r1),
                                                                 h.xor(and_triple_A.r2, and_triple_B.r2))))
            if and_triple_B.r3 == b'\x01':
                and_triple_B.M3 = bytes(h.xor(and_triple_A.K3, delta_a))
            else:
                and_triple_B.M3 = and_triple_A.K3
            if and_triple_A.r3 == b'\x01':
                and_triple_B.K3 = bytes(h.xor(and_triple_A.M3, delta_b))
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

            conn2.send(b'\x02' + and_triple_B.SerializeToString())
            conn1.send(b'\x02')
        elif data_A == b'\xfe':
            conn1.close()
            conn2.close()
            run = False
