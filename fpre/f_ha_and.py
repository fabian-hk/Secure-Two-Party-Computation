from tools import communication
from random import randint
from tools.person import Person
import os
from random import randint
import conf
import socket
import tools.helper as h
from tools.person import Person
from tools import communication
from fpre import fpre
import hashlib


def f_ha_and(person, own_y_bit):
    '''

    :param person:
    :param own_y_bit:
    :return:
    '''


    Communicator = communication.Com()


    #TODO get values from F_abit


    own_x_bit = 0
    own_x_mac = 0
    opp_x_key = 0

    random_bit = randint(0,1)



    hash_function = hashlib.sha3_256()
    hash_function.update(opp_x_key)
    H_0 = abs(get_lsb(hash_function.digest()) - random_bit)
    hash_function.update(h.xor(opp_x_key, person.delta))
    tmp_0 = hash_function.digest()
    tmp_1 = abs(tmp_0 - random_bit)
    H_1 = abs(tmp_1 - own_y_bit)

    opp_H_0 = Communicator.exchange_data(310, H_0)
    opp_H_1 = Communicator.exchange_data(311, H_1)

    H_x = None

    if own_x_bit == 0:
        H_x = opp_H_0
    elif own_x_bit == 1:
        H_x = opp_H_1
    else:
        raise TypeError
    hash_function.update(own_x_mac)


    tmp_result = abs(H_x - get_lsb(hash_function.digest()))
    return abs(random_bit - tmp_result)



#return least significant byte and calculates the lsb afterwards
def get_lsb(bytes):
    '''
    returns least significant bit of bytes input
    :param bytes:
    :return int: digit 0 or 1
    '''
    a = ["{0:b}".format(e) for e in bytes]
    least_significant_byte  = a[-1]
    result = least_significant_byte[-1]
    if result.isdigit():
        return int(result)
    else:
        raise TypeError
