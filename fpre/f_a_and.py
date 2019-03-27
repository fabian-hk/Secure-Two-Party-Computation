from random import randint
import json

from fpre.f_la_and import f_la_and
from tools.person import Person
from fpre.fpre import Fpre
from protobuf import FunctionDependentPreprocessing_pb2
import conf

buckets = conf.upper_bound_gates
objects_per_bucket = 10


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
    other_half = json.load(ser_other_half.decode('utf-8'))

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
    for i in full_list:
        if i % buckets == 0:
            and_triple_out = and_triples_out.triples.add()
            and_triple_out = and_triple_dict[i]
        else:
            combine_two_leaky_and(and_triple_out, and_triple_dict[i])

    return and_triples_out


def combine_two_leaky_and(and_triple_0, and_triple_1):
    pass
