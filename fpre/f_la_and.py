import os
from random import randint
import conf
import socket
import tools.helper as h
from tools.person import Person
from tools import communication
import hashlib



import sys

#****************** PI LA AND **************************
#autheticated bit: [b]A PA -> (M[b],b)   |PB -> (K[b],delta)
#autheticated bit: [b]B PB -> (M[b],b)   |PA -> (K[b],delta)



def f_la_and(person):

    Communicator = communication.Com(person)


    #***_STEP__1__***
    #init
    own_x_bit = 0               #wrong
    own_x_mac = person.delta    #wrong but correct datataype

    own_y_bit = 0               #wrong
    own_y_mac = person.delta    #wrong but correct datataype


    opp_x_key = person.delta    #wrong but correct datatype

    opp_y_key = person.delta    #wrong but correct datatype

    own_z_bit = None
    own_z_mac = None

    own_r_bit = None
    own_r_mac = None

    opp_z_key = None
    opp_r_key = None

    if person.x == person.A:
        own_z_bit = 0               #wrong
        own_z_mac = person.delta    #wrong

        opp_r_key = person.delta    #wrong

    else:
        own_r_bit = 0               #wrong
        own_r_mac = person.delta    #wrong but correct datatype

        opp_z_key = person.delta    #wrong but correct datatype
    #...
    #...
    #...
    v_1 = person.delta              #wrong but correct datatype
    v_2 = person.delta              #wrong but correct datatype


    # ***_STEP__3__***
    u = None

    if person.x == person.A:
        if own_x_bit == 1 and own_y_bit == 1:
            u = abs(v_1 - 1)
        else:
            u = v_1
        nothing = Communicator.exchange_data(230, u)
        d = Communicator.exchange_data(231)
        #TODO commpute opp_z_key


    if person.x == person.B:
        tmp = None
        u = Communicator.exchange_data(230)
        own_z_bit = None
        if own_x_bit == 1 and own_y_bit == 1:
            tmp = abs(u - 1)
        else:
            tmp = u
        own_z_bit = abs(u - v_2)

        d = abs(own_r_bit - own_z_bit)
        nothing = Communicator.exchange_data(231, d)
        #TODO compute own_z_mac


    U = []
    # ***_STEP__4-5__***
    #check correctness
    #(a)
    hash_function = hashlib.sha3_256()
    if own_z_bit == 1:
        hash_function.update(opp_x_key + h.xor(opp_z_key, person.delta))
    else:
        hash_function.update(opp_x_key + opp_z_key)
    T_0 = hash_function.digest()

    if bool(own_y_bit) != bool(own_y_bit):
        hash_function.update(h.xor(opp_x_key, person.delta) +  h.xor(opp_y_key, opp_z_key, person.delta))
    else:
        hash_function.update(opp_x_key + h.xor(opp_y_key, opp_z_key))
    U.append(h.xor(T_0, hash_function.digest()))

    if bool(own_y_bit) != bool(own_y_bit):
        tmp_funct = h.xor(h.xor(opp_y_key, opp_z_key, person.delta))
    else:
        tmp_funct = h.xor(h.xor(opp_y_key, opp_z_key))

    hash_function.update(opp_x_key + tmp_funct)
    T_1 = hash_function.digest()

    if own_z_bit == 1:
        hash_function.update(h.xor(opp_x_key, person.delta) + h.xor(opp_z_key, person.delta))
    else:
        hash_function.update(h.xor(opp_x_key, person.delta) + opp_z_key)
    U.append(h.xor(T_1, hash_function.digest()))

    #(b)
    if own_x_bit < 2 and own_x_bit >= 0:
        U_solid = Communicator.exchange_data(240, U[own_x_bit])
    else:
        raise TypeError

    #(c)
    #pick random k-bit string
    R_size = len(T_1)
    R = os.urandom(R_size)
    V = []

    #V0
    hash_function.update(own_x_mac + own_z_mac)
    V.append(hash_function.digest())
    #V1
    hash_function.update(own_x_mac +  h.xor(own_z_mac, own_y_mac))
    V.append(hash_function.update())


    W = []
    hash_function.update(opp_x_key)
    hash_key_x = hash_function.digest()
    hash_function.update(h.xor(opp_x_key, person.delta))
    hash_key_x_xor = hash_function.digest()
    W_0_0 = h.xor(hash_key_x,  V[0], R)
    W_0_1 = h.xor(hash_key_x_xor,  V[0], R)
    W_1_0 = h.xor(hash_key_x, V[1], U_solid, R)
    W_1_1 = h.xor(hash_key_x_xor, V[1], U_solid, R)

    #(d)

    W_opp_x_0 = None
    W_opp_x_1 = None
    if own_x_bit == 0:
        W_opp_x_0 = Communicator.exchange_data(241, W_0_0)
        W_opp_x_1 = Communicator.exchange_data(242, W_0_1)
    elif own_x_bit == 1:
        W_opp_x_0 = Communicator.exchange_data(241, W_1_0)
        W_opp_x_1 = Communicator.exchange_data(242, W_1_1)
    else:
        raise TypeError

    #TODO send R to FEQ

    #(e)

    W_x_x = None
    if own_x_bit == 0:
        W_x_x = W_opp_x_0
    elif own_x_bit == 1:
        W_x_x = W_opp_x_1
    else:
        raise TypeError


    hash_function.update(own_x_mac)
    R_new = None
    if own_x_bit == 0:
        R_new = h.xor(W_x_x, hash_function.digest(), T_0)
    elif own_x_bit == 1:
        R_new = h.xor(W_x_x, hash_function.digest(), T_1)
    else:
        raise TypeError

    #TODO send R_new to FEQ






def f_ha_and(y):
    return 0

def f_eq(x):
    return True

