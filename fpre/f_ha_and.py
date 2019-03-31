from tools import communication
from random import randint
from tools.person import Person
import os
from random import randint
import conf
import socket
import tools.helper as h
from tools.person import Person
from fpre.fpre import Fpre


def f_ha_and(person: Person, communicator: Fpre,  own_y_bit):
    '''

    :param person:
    :param own_y_bit:
    :return:
    '''





    #TODO get values from F_abit
    auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
    if person.x == Person.A:
        for i in range(3):
            auth_bit = auth_bits.bits.add()
            auth_bit.id = i
            communicator.authenticated_bit(auth_bit)

        communicator.send_auth_bits(auth_bits.SerializeToString())
    else:
        auth_bits.ParseFromString(communicator.rec_auth_bits())
        auth_bit = iter(auth_bits).__next__()


    own_x_bit = auth_bit.r
    own_x_mac = auth_bit.M
    opp_x_key = auth_bit.K

    random_bit = randint(0,1)



    hash_function = hashlib.sha3_512()
    hash_function.update(opp_x_key)
    H_0 = abs(get_lsb(hash_function.digest()) - random_bit)

    hash_function = hashlib.sha3_512()
    hash_function.update(h.xor(opp_x_key, person.delta))
    tmp_0 = hash_function.digest()

    tmp_1 = abs(get_lsb(tmp_0) - random_bit)
    H_1 = abs(tmp_1 - own_y_bit)

    opp_H_0 = communicator.exchange_data(310, H_0)
    opp_H_1 = communicator.exchange_data(311, H_1)

    H_x = None

    if own_x_bit == 0:
        H_x = opp_H_0
    elif own_x_bit == 1:
        H_x = opp_H_1
    else:
        raise TypeError
    hash_function = hashlib.sha3_512()
    hash_function.update(own_x_mac)




    tmp_result = abs(H_x - get_lsb(hash_function.digest()))
    return abs(random_bit - tmp_result), auth_bit



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

