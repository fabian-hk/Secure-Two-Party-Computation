from random import randint
import json

# from fpre.f_la_and import f_la_and
from tools.person import Person
from fpre.fpre import Fpre
from protobuf import FunctionDependentPreprocessing_pb2, FunctionIndependentPreprocessing_pb2
import tools.helper as h
import conf
from protobuf import Wrapper

buckets = conf.upper_bound_gates
objects_per_bucket = 10


# ******* just for testing ********
def f_la_and(com, person, and_triple):
    auth_bits = FunctionIndependentPreprocessing_pb2.AuthenticatedBits()
    if person.x == Person.A:
        for i in range(3):
            auth_bit = auth_bits.bits.add()
            auth_bit.id = i
            com.authenticated_bit(auth_bit)
        com.send_auth_bits(auth_bits.SerializeToString())
    else:
        auth_bits.ParseFromString(com.rec_auth_bits())

    auth_bits_iter = iter(auth_bits.bits)
    auth_bit = Wrapper.get_auth_bit_by_id(0, auth_bits)
    and_triple.r1 = auth_bit.r
    and_triple.M1 = auth_bit.M
    and_triple.K1 = auth_bit.K
    auth_bit = Wrapper.get_auth_bit_by_id(1, auth_bits)
    and_triple.r2 = auth_bit.r
    and_triple.M2 = auth_bit.M
    and_triple.K2 = auth_bit.K
    if person.x == Person.A:
        auth_bit = Wrapper.get_auth_bit_by_id(2, auth_bits)
        and_triple.r3 = auth_bit.r
        and_triple.M3 = auth_bit.M
        and_triple.K3 = auth_bit.K

    if person.x == Person.A:
        com.and_triples(and_triple.SerializeToString())
    else:
        and_triple.ParseFromString(com.and_triples(and_triple.SerializeToString()))


# **********************************

def f_a_and(person, com: Fpre):
    # **** step_1 ****
    l_dash = buckets * objects_per_bucket

    and_triples_out = FunctionDependentPreprocessing_pb2.ANDTriples()

    and_triples = FunctionDependentPreprocessing_pb2.ANDTriples()
    for i in range(l_dash):
        and_triple = and_triples.triples.add()
        and_triple.id = i
        f_la_and(com, person, and_triple)

    # **** step_2 ****
    # partition objects random in buckets
    half_list = []
    for i in range(int(l_dash / 2)):
        n = randint(0, int(l_dash / 2)) if person.x == Person.A else randint(int(l_dash / 2) + 1, l_dash)
        while n in half_list:
            n = randint(0, int(l_dash / 2)) if person.x == Person.A else randint(int(l_dash / 2) + 1, l_dash)
        half_list.append(n)

    ser_half_list = json.dumps(half_list).encode('utf-8')
    ser_other_half = com.exchange_data(ser_half_list)
    other_half = json.loads(ser_other_half.decode('utf-8'))

    full_list = []
    iter_half_list = iter(half_list)
    iter_other_list = iter(other_half)
    p = next(iter_half_list, None) if person.x == Person.A else next(iter_other_list, None)
    q = next(iter_other_list, None) if person.x == Person.A else next(iter_half_list, None)
    while p or q:
        full_list.append(p)
        full_list.append(q)
        p = next(iter_half_list, None) if person.x == Person.A else next(iter_other_list, None)
        q = next(iter_other_list, None) if person.x == Person.A else next(iter_half_list, None)

    and_triple_dict = {}
    for pos, and_triple in zip(full_list, and_triples.triples):
        and_triple_dict[pos] = and_triple

    # **** step_3 ****
    j = 0
    for i in full_list:
        if j % objects_per_bucket == 0:
            and_triple_out = and_triples_out.triples.add()
            and_triple_out = and_triple_dict[i]
        else:
            combine_two_leaky_and(and_triple_out, and_triple_dict[i], com, person)
        j += 1

    return and_triples_out


def combine_two_leaky_and(and_triple_out, and_triple, com: Fpre, person: Person):
    auth_bit = FunctionIndependentPreprocessing_pb2.Bit()
    auth_bit.id = and_triple.id
    d_dash = h.xor(and_triple_out.r2, and_triple.r2)  # TODO what does with their MAC checked mean?
    auth_bit.r = bytes(d_dash)
    auth_bit.M = bytes(h.xor(and_triple_out.M2, and_triple.M2))
    auth_bit.ParseFromString(com.exchange_data(auth_bit.SerializeToString()))
    d_dash_2 = auth_bit.r

    # check the MAC
    if d_dash_2 == b'\x01':
        if auth_bit.M == bytes(h.xor(and_triple_out.K2, and_triple.K2, person.delta)):
            print("Combine leaky and: Check correct.")
        else:
            print("Combine leaky and: Check cheat.")
    else:
        if auth_bit.M == bytes(h.xor(and_triple_out.K2, and_triple.K2)):
            print("Combine leaky and: Check correct.")
        else:
            print("Combine leaky and: Check cheat.")

    d = h.xor(d_dash, d_dash_2)

    # combine x1
    and_triple_out.r1 = bytes(h.xor(and_triple_out.r1, and_triple.r1))
    and_triple_out.M1 = bytes(h.xor(and_triple_out.M1, and_triple.M1))
    and_triple_out.K1 = bytes(h.xor(and_triple_out.K1, and_triple.K1))

    # combine x2 pass TODO b) [y2]A error in protocol?
    # combine x3
    if d == b'\x01':
        and_triple_out.r3 = bytes(h.xor(and_triple_out.r3, and_triple.r3, and_triple.r1))
        and_triple_out.M3 = bytes(h.xor(and_triple_out.M3, and_triple.M3, and_triple.M1))
        and_triple_out.K3 = bytes(h.xor(and_triple_out.K3, and_triple.K3, and_triple.K1))
    else:
        and_triple_out.r3 = bytes(h.xor(and_triple_out.r3, and_triple.r3))
        and_triple_out.M3 = bytes(h.xor(and_triple_out.M3, and_triple.M3))
        and_triple_out.K3 = bytes(h.xor(and_triple_out.K3, and_triple.K3))


if __name__ == "__main__":
    com = Fpre('localhost', 8448)
    f_a_and(com.person, com)
