import os
from random import randint
import conf
import socket
import hashlib

import tools.helper as h
from tools.person import Person
from fpre.fpre import Fpre
from protobuf import FunctionDependentPreprocessing_pb2, FunctionIndependentPreprocessing_pb2

from fpre.f_eq import f_eq as f_eq
from fpre import f_ha_and

from exceptions.CheaterException import Cheater_recognized

import sys

#****************** PI LA AND **************************
#autheticated bit: [b]A PA -> (M[b],b)   |PB -> (K[b],delta)
#autheticated bit: [b]B PB -> (M[b],b)   |PA -> (K[b],delta)



def f_la_and(communicator: Fpre, person: Person, and_triple: FunctionIndependentPreprocessing_pb2.AuthenticatedBits):
    if and_triple.r1 == bytes(0):
        auth_bits = get_authbits(person, communicator, 3)
        auth_bits_iter = iter(auth_bits.bits)

        auth_bit = next(auth_bits_iter)
        own_x_bit = auth_bit.r
        own_x_mac = auth_bit.M
        opp_x_key = auth_bit.K
        auth_bit = next(auth_bits_iter)
        own_y_bit = auth_bit.r
        own_y_mac = auth_bit.M
        opp_y_key = auth_bit.K

        if person.x == person.A:
            auth_bit = next(auth_bits_iter)
            own_z_bit = auth_bit.r
            own_z_mac = auth_bit.M
            opp_r_key = auth_bit.K
        else:
            auth_bit = next(auth_bits_iter)
            own_r_bit = auth_bit.r
            own_r_mac = auth_bit.M
            opp_z_key = auth_bit.K
    else:
        own_x_bit = and_triple.r1
        own_x_mac = and_triple.M1
        opp_x_key = and_triple.K1
        own_y_bit = and_triple.r2
        own_y_mac = and_triple.M2
        opp_y_key = and_triple.K2

        auth_bits = get_authbits(person, communicator, 1)
        auth_bits_iter = iter(auth_bits.bits)

        if person.x == person.A:
            auth_bit = next(auth_bits_iter)
            own_z_bit = auth_bit.r
            own_z_mac = auth_bit.M
            opp_r_key = auth_bit.K
        else:
            auth_bit = next(auth_bits_iter)
            own_r_bit = auth_bit.r
            own_r_mac = auth_bit.M
            opp_z_key = auth_bit.K

    v = f_ha_and.f_ha_and(person, own_y_bit)

    # ***_STEP__3__***
    if person.x == person.A:
        u = h.xor(v, h.AND(own_x_bit, own_y_bit))
        nothing = communicator.exchange_data(u)
        d = communicator.exchange_data()

        if d == 0:
            opp_d_key = int(0).to_bytes(len(person.delta), byteorder='big')
        else:
            opp_d_key = person.delta

        opp_z_key = h.xor(opp_d_key, opp_r_key)

    if person.x == person.B:
        u = communicator.exchange_data()
        own_z_bit = h.xor(u, v, h.AND(own_x_bit, own_y_bit))
        d = h.xor(own_r_bit, own_z_bit)
        communicator.exchange_data(d)
        own_z_mac = own_r_mac

    U = []
    # ***_STEP__4-5__***
    #check correctness
    #(a)
    if own_z_bit == 1:
        hash_function = hashlib.sha3_512()
        hash_function.update(opp_x_key + h.xor(opp_z_key, person.delta))
    else:
        hash_function = hashlib.sha3_512()
        hash_function.update(opp_x_key + opp_z_key)
    T_0 = hash_function.digest()

    if h.xor(own_y_bit, own_z_bit) == b'\x01':
        hash_function = hashlib.sha3_512()
        hash_function.update(h.xor(opp_x_key, person.delta) +  h.xor(opp_y_key, opp_z_key, person.delta))
    else:
        hash_function = hashlib.sha3_512()
        hash_function.update(opp_x_key + h.xor(opp_y_key, opp_z_key))
    U.append(h.xor(T_0, hash_function.digest()))

    if h.xor(own_y_bit, own_z_bit) == b'\x01':
        tmp_funct = h.xor(opp_y_key, opp_z_key, person.delta)
    else:
        tmp_funct = h.xor(opp_y_key, opp_z_key)

    hash_function = hashlib.sha3_512()
    hash_function.update(opp_x_key + tmp_funct)
    T_1 = hash_function.digest()

    if own_z_bit == 1:
        hash_function = hashlib.sha3_512()
        hash_function.update(h.xor(opp_x_key, person.delta) + h.xor(opp_z_key, person.delta))
    else:
        hash_function = hashlib.sha3_512()
        hash_function.update(h.xor(opp_x_key, person.delta) + opp_z_key)
    U.append(h.xor(T_1, hash_function.digest()))

    #(b)
    if own_x_bit < 2 and own_x_bit >= 0:
        U_solid = communicator.exchange_data(U[own_x_bit])
    else:
        raise TypeError()

    #(c)
    #pick random k-bit string
    R_size = len(T_1)
    R = os.urandom(R_size)
    V = []

    #V0
    hash_function = hashlib.sha3_512()
    hash_function.update(own_x_mac + own_z_mac)
    V.append(hash_function.digest())
    #V1
    hash_function = hashlib.sha3_512()
    hash_function.update(own_x_mac +  h.xor(own_z_mac, own_y_mac))
    V.append(hash_function.update())

    W = []
    hash_function = hashlib.sha3_512()
    hash_function.update(opp_x_key)
    hash_key_x = hash_function.digest()
    hash_function = hashlib.sha3_512()
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
        W_opp_x_0 = communicator.exchange_data(W_0_0)
        W_opp_x_1 = communicator.exchange_data(W_0_1)
    elif own_x_bit == 1:
        W_opp_x_0 = communicator.exchange_data(W_1_0)
        W_opp_x_1 = communicator.exchange_data( W_1_1)
    else:
        raise TypeError

    r_eq = f_eq(person, communicator, R)

    #(e)

    W_x_x = None
    if own_x_bit == 0:
        W_x_x = W_opp_x_0
    elif own_x_bit == 1:
        W_x_x = W_opp_x_1
    else:
        raise TypeError()

    hash_function = hashlib.sha3_256()
    hash_function.update(own_x_mac)
    R_new = None
    if own_x_bit == 0:
        R_new = h.xor(W_x_x, hash_function.digest(), T_0)
    elif own_x_bit == 1:
        R_new = h.xor(W_x_x, hash_function.digest(), T_1)
    else:
        raise TypeError()



    r_new_eq = f_eq(person, communicator, R_new)
    if r_eq and r_new_eq:
        pass
    else:
        raise Cheater_recognized()

    and_triple.r1 = own_x_bit
    and_triple.r2 = own_y_bit
    and_triple.r3 = own_z_bit

    and_triple.M1 = own_x_mac
    and_triple.M2 = own_y_mac
    and_triple.M3 = own_z_mac

    and_triple.K1 = opp_x_key
    and_triple.K2 = opp_y_key
    and_triple.K3 = opp_z_key


def get_authbits(person: Person, communicator: Fpre, number):
    auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
    if person.x == Person.A:
        for i in range(number):
            auth_bit = auth_bits.bits.add()
            auth_bit.id = i
            communicator.authenticated_bit(auth_bit)
        communicator.send_auth_bits(auth_bits.SerializeToString())
    else:
        auth_bits.ParseFromString(communicator.rec_auth_bits())

    return auth_bits

