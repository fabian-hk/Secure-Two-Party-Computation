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

from exceptions.CheaterException import CheaterRecognized

import sys


# ****************** PI LA AND **************************
# autheticated bit: [b]A PA -> (M[b],b)   |PB -> (K[b],delta)
# autheticated bit: [b]B PB -> (M[b],b)   |PA -> (K[b],delta)


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

        if person.x == Person.A:
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

        if person.x == Person.A:
            auth_bit = next(auth_bits_iter)
            own_z_bit = auth_bit.r
            own_z_mac = auth_bit.M
            opp_r_key = auth_bit.K
        else:
            auth_bit = next(auth_bits_iter)
            own_r_bit = auth_bit.r
            own_r_mac = auth_bit.M
            opp_z_key = auth_bit.K

    v = f_ha_and.f_ha_and(person, communicator, own_y_bit, own_x_bit, own_x_mac, opp_x_key)

    # ***_STEP__3__***
    if person.x == Person.A:
        u = h.xor(v, h.AND(own_x_bit, own_y_bit), own_z_bit) # TODO discuss own fix
        nothing = communicator.exchange_data(u)
        d = communicator.exchange_data()

        if d == b'\x00':
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

    # save and_triple in protobuf message
    and_triple.r1 = own_x_bit
    and_triple.M1 = own_x_mac
    and_triple.K1 = opp_x_key
    and_triple.r2 = own_y_bit
    and_triple.M2 = own_y_mac
    and_triple.K2 = opp_y_key
    and_triple.r3 = bytes(own_z_bit)
    and_triple.M3 = bytes(own_z_mac)
    and_triple.K3 = bytes(opp_z_key)

    return

    # ***_STEP__4-5__***
    # check correctness
    # (a)
    if own_z_bit == b'\x01':
        hash_function = hashlib.sha3_256()
        hash_function.update(opp_x_key + h.xor(opp_z_key, person.delta))
        T_0 = hash_function.digest()
    else:
        hash_function = hashlib.sha3_256()
        hash_function.update(opp_x_key + opp_z_key)
        T_0 = hash_function.digest()

    if h.xor(own_y_bit, own_z_bit) == b'\x01':
        hash_function = hashlib.sha3_256()
        hash_function.update(h.xor(opp_x_key, person.delta) + h.xor(opp_y_key, opp_z_key, person.delta))
        U_0 = bytes(h.xor(T_0, hash_function.digest()))

    else:
        hash_function = hashlib.sha3_256()
        hash_function.update(h.xor(opp_x_key, person.delta) + h.xor(opp_y_key, opp_z_key))
        U_0 = bytes(h.xor(T_0, hash_function.digest()))

    if h.xor(own_y_bit, own_z_bit) == b'\x01':
        tmp_funct = h.xor(opp_y_key, opp_z_key, person.delta)
    else:
        tmp_funct = h.xor(opp_y_key, opp_z_key)

    hash_function = hashlib.sha3_256()
    hash_function.update(opp_x_key + tmp_funct)
    T_1 = hash_function.digest()

    if own_z_bit == 1:
        hash_function = hashlib.sha3_256()
        hash_function.update(h.xor(opp_x_key, person.delta) + h.xor(opp_z_key, person.delta))
        U_1 = bytes(h.xor(T_1, hash_function.digest()))
    else:
        hash_function = hashlib.sha3_256()
        hash_function.update(h.xor(opp_x_key, person.delta) + opp_z_key)
        U_1 = bytes(h.xor(T_1, hash_function.digest()))

    # (b)
    if own_x_bit == b'\x00':
        U_solid = communicator.exchange_data(U_0)

    elif own_x_bit == b'\x01':
        U_solid = communicator.exchange_data(U_1)
    else:
        raise TypeError()

    # (c)
    # pick random k-bit string
    R = os.urandom(int(conf.k / 8))
    V = []

    # V0
    hash_function = hashlib.sha3_256()
    hash_function.update(own_x_mac + own_z_mac)
    V_0 = hash_function.digest()
    # V1
    hash_function = hashlib.sha3_256()
    hash_function.update(own_x_mac + h.xor(own_z_mac, own_y_mac))
    V_1 = hash_function.digest()

    W = []
    hash_function = hashlib.sha3_256()
    hash_function.update(opp_x_key)
    hash_key_x = hash_function.digest()
    hash_function = hashlib.sha3_256()
    hash_function.update(h.xor(opp_x_key, person.delta))
    hash_key_x_xor = hash_function.digest()
    W_0_0 = bytes(h.xor(hash_key_x, V_0, R))
    W_0_1 = bytes(h.xor(hash_key_x_xor, V_1, R))
    W_1_0 = bytes(h.xor(hash_key_x, V_1, U_solid, R))
    W_1_1 = bytes(h.xor(hash_key_x_xor, V_0, U_solid, R))

    # (d)
    if own_x_bit == b'\x00':
        W_opp_x_0 = communicator.exchange_data(W_0_0)
        W_opp_x_1 = communicator.exchange_data(W_0_1)
    elif own_x_bit == b'\x01':
        W_opp_x_0 = communicator.exchange_data(W_1_0)
        W_opp_x_1 = communicator.exchange_data(W_1_1)
    else:
        raise TypeError

    # (e)
    if own_x_bit == b'\x00':
        W_x_x = W_opp_x_0
    elif own_x_bit == b'\x01':
        W_x_x = W_opp_x_1
    else:
        raise TypeError()

    hash_function = hashlib.sha3_256()
    hash_function.update(own_x_mac)
    # R_new = None
    if own_x_bit == b'\x00':
        R_new = bytes(h.xor(W_x_x, hash_function.digest(), T_0))
    elif own_x_bit == b'\x01':
        R_new = bytes(h.xor(W_x_x, hash_function.digest(), T_1))
    else:
        raise TypeError()

    if person.x == Person.A:
        # PA sends first R then R'
        r_pa_a_dash_b = f_eq(person, communicator, R)
        r_dash_a_r_b = f_eq(person, communicator, R_new)
    else:
        r_pa_a_dash_b = f_eq(person, communicator, R_new)
        r_dash_a_r_b = f_eq(person, communicator, R)

    if r_pa_a_dash_b and r_dash_a_r_b:
        print("r_eq equals r_new_eq")
    else:
        print("cheat")
        # raise CheaterRecognized()
    '''
    and_triple.r1 = own_x_bit
    and_triple.M1 = own_x_mac
    and_triple.K1 = opp_x_key
    and_triple.r2 = own_y_bit
    and_triple.M2 = own_y_mac
    and_triple.K2 = opp_y_key
    and_triple.r3 = bytes(own_z_bit)
    and_triple.M3 = bytes(own_z_mac)
    and_triple.K3 = bytes(opp_z_key)
    '''


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
