import os
from random import randint
import conf
import socket
from tools.person import Person

TCP_IP = 'localhost'
TCP_PORT = 3003
BUFFER_SIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def init_a(person: Person):
    s.connect((TCP_IP, TCP_PORT))
    s.send(b'\x00' + person.delta)
    s.recv(BUFFER_SIZE)


def init_b():
    s.connect((TCP_IP, TCP_PORT))
    delta = s.recv(BUFFER_SIZE)
    return delta


# ********** create authenticated bits *************
def authenticated_bit(auth_bit):
    r = randint(0, 1)
    M = os.urandom(conf.k)
    K = os.urandom(conf.k)
    auth_bit.r = r.to_bytes(1, "big")
    auth_bit.M = M
    auth_bit.K = K
    return r, M, K


def send_auth_bits(data):
    print("send data: "+str(len(data)))
    s.send(b'\x01' + data)
    s.recv(BUFFER_SIZE)
# *************************************************
