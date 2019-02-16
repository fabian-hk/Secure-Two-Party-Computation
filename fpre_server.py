import socket
import os
import conf
from protobuf import FunctionIndependentPreprocessing_pb2, FunctionDependentPreprocessing_pb2

TCP_IP = 'localhost'
TCP_PORT = 3003
BUFFER_SIZE = 4096

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
        delta_b = os.urandom(conf.k)
        conn2.send(delta_b)
        conn1.send(b'\x00')
    elif data[0] == 1:
        auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBit()
        auth_bits.ParseFromString(data[1:])
        for auth_bit in auth_bits.bits:
            print("ID: "+str(auth_bit.id))
            print("\tr: "+str(auth_bit.r))
            print("\tM: "+str(auth_bit.M))
            print("\tK: "+str(auth_bit.K))
            print()
