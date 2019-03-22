import os
from random import randint
import conf
import socket
import tools.helper as h
from tools.person import Person
from tools import f_la_and
import hashlib


import sys

TCP_IP = 'localhost'
TCP_PORT = 3003
BUFFER_SIZE = 42 * (conf.upper_bound_gates + 2 * conf.input_size)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


hash_function = hashlib.sha3_256()


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






#****************** PI LA AND **************************
#autheticated bit: [b]A PA -> (M[b],b)   |PB -> (K[b],delta)
#autheticated bit: [b]B PB -> (M[b],b)   |PA -> (K[b],delta)



random_autheticated_bit_y = 0



x_1 = 0
y_1 = 0
z_1 = 0
x_2 = 0
y_2 = 0
r = 0











def f_la_and_A(person, v_1):
    #********step 3*************
    u = h.xor(v_1, h.AND(x_1, y_1))
    #send u to b
    #recv d from PB



    s.connect((TCP_IP, TCP_PORT))
    s.send(b'\x00')
    s.recv(BUFFER_SIZE)




def f_la_and_B(person, v_2):

    #******step 3*********
    #u = s.recv(BUFFER_SIZE) - get u from PA
    u = 0
    z_2 = h.xor(u, h.AND(x_2, y_2), v_2)
    d = h.xor(r, z_2)
    #send d to PA

    #******step_4***********
    #a
    hash_function = hashlib.sha3_256()
    if z_2.x == 0:
        hash_function.update(x_1.k + h.xor(z_1.k, person.delta))
        T_0 = hash_function.digest()
    else:
        hash_function.update(x_1.k +z_1.k)
        T_0 = hash_function.digest()

    s.connect((TCP_IP, TCP_PORT))
    s.send(b'\x00')
    s.recv(BUFFER_SIZE)






def f_la_and(person):
    #print(person.x == person.A)
    #print(person.delta)
    #y is own value -> sends v to the other party
    #************step2***********************
    v = f_ha_and(random_autheticated_bit_y)
    #*******to_step_3********* - split
    if person.x == person.A:
        f_la_and_A(person, v)
    elif person.x == person.B:
        f_la_and_B(person, v)
    else:
        #not person A nor B
        raise RuntimeError



def f_ha_and(y):
    return 0

def f_eq(x):
    return True

