import socket
import os
import conf
import tools.helper as h
from random import randint
from protobuf import FunctionIndependentPreprocessing_pb2, FunctionDependentPreprocessing_pb2

TCP_IP = 'localhost'
TCP_PORT = 3003
BUFFER_SIZE = 42 * (conf.upper_bound_gates + 2 * conf.input_size)

delta_a = None
delta_b = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

conn1, addr1 = s.accept()
print("First connection. IP: " + str(addr1))

conn2, addr2 = s.accept()
print("Second connection. IP: " + str(addr2))

while True:
    data = conn1.recv(BUFFER_SIZE)
    if not data:
        continue
    if data[0] == 0:
        delta_a = data[1:]
        delta_b = os.urandom(int(conf.k/8))
        conn2.send(b'\x00' + delta_b)
        conn1.send(b'\x00')
    elif data[0] == 1:
        auth_bits_A = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
        auth_bits_B = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
        auth_bits_A.ParseFromString(data[1:])
        for auth_bit_A in auth_bits_A.bits:
            auth_bit_B = auth_bits_B.bits.add()
            s = randint(0, 1)
            auth_bit_B.r = s.to_bytes(1, 'big')
            if s == 0:
                auth_bit_B.K = auth_bit_A.M
                auth_bit_B.M = auth_bit_A.K
            else:
                auth_bit_B.K = bytes(h.xor(auth_bit_A.M, delta_b))
                auth_bit_B.M = bytes(h.xor(auth_bit_A.K, delta_a))
        ser_auth_bits = auth_bits_B.SerializeToString()
        conn2.send(b'\x01' + ser_auth_bits)
        conn1.send(b'\x01')
