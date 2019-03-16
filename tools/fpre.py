import os
from random import randint
import conf
import socket
from tools.person import Person
import sys

TCP_IP = 'localhost'
TCP_PORT = 3003
BUFFER_SIZE = 42 * (conf.upper_bound_gates + 2 * conf.input_size)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# *************** Initialization ******************
def init_a(person: Person):
    s.connect((TCP_IP, TCP_PORT))
    s.send(b'\x00' + person.delta)
    s.recv(BUFFER_SIZE)


def init_b():
    s.connect((TCP_IP, TCP_PORT))
    data = s.recv(BUFFER_SIZE)
    if data[0] == 0:
        return data[1:]
    else:
        sys.exit(1)


# ********** create authenticated bits *************
def authenticated_bit(auth_bit):
    r = randint(0, 1)
    M = os.urandom(int(conf.k / 8))
    K = os.urandom(int(conf.k / 8))
    auth_bit.r = r.to_bytes(1, "big")
    auth_bit.M = M
    auth_bit.K = K
    return r, M, K


def send_auth_bits(data):
    print("send data: " + str(len(data)))
    s.send(b'\x01' + data)
    print(data)
    s.recv(BUFFER_SIZE)


def rec_auth_bits():
    data = s.recv(BUFFER_SIZE)
    print("Rec auth bits: "+str(len(data[1:])))
    if data[0] == 1:
        return data[1:]


# ***************** AND triples ********************
def and_triples(data: bytes):
    s.send(b'\x02'+data)
    return_data = s.recv(BUFFER_SIZE)
    if return_data[0] == 2:
        return return_data[1:]
