from tools import communication
from random import randint
from tools.person import Person
import os
import hashlib

from random import randint
import conf
import socket
import tools.helper as h
from tools.person import Person
from fpre.fpre import Fpre
from protobuf import FunctionIndependentPreprocessing_pb2


def f_ha_and(person: Person, communicator: Fpre, own_y_bit, own_x_bit, own_x_mac, opp_x_key):
    """
    :param person:
    :param communicator:
    :param own_y_bit:
    :param own_x_bit:
    :param own_x_mac:
    :param own_x_key:
    :return:
    """
    random_bit = randint(0, 1).to_bytes(1, "big")

    hash_function = hashlib.sha3_512()
    hash_function.update(opp_x_key)
    H_0 = h.xor(get_lsb(hash_function.digest()), random_bit)

    hash_function = hashlib.sha3_512()
    hash_function.update(h.xor(opp_x_key, person.delta))

    H_1 = h.xor(get_lsb(hash_function.digest()), own_y_bit, random_bit)

    opp_H_0 = communicator.exchange_data(H_0)
    opp_H_1 = communicator.exchange_data(H_1)

    H_x = None

    if own_x_bit == b'\00':
        H_x = opp_H_0
    elif own_x_bit == b'\x01':
        H_x = opp_H_1
    else:
        raise TypeError
    hash_function = hashlib.sha3_512()
    hash_function.update(own_x_mac)

    result_bit = h.xor(H_x, get_lsb(hash_function.digest()), random_bit)

    return get_lsb(result_bit)


def get_lsb(input_bytes):
    '''
    returns least significant bit of bytes input
    :param input_bytes:
    :return byte: b'\x00' or b'\x01'
    '''
    a = ["{0:b}".format(e) for e in input_bytes]
    least_significant_byte = a[-1]
    result = least_significant_byte[-1]
    byteArray = bytearray()
    if result.isdigit():
        if int(result) == 0:
            return b'\x00'
        else:
            return b'\x01'
    else:
        raise TypeError


def get_least_byte(input_bytes):
    a = ["{0:b}".format(e) for e in input_bytes]
    return a[-1]
