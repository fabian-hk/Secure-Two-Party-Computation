import fpre.f_la_and as flaand
from tools.person import Person
from random import randint

from fpre.fpre import Fpre
from protobuf import FunctionDependentPreprocessing_pb2

buckets = 10
objects_per_bucket = 10


def f_a_and(person, communicator: Fpre):
    # communicator.exchange_data(bytes)

    l_dash = buckets * objects_per_bucket

    all_objects = []
    # person = Person(Person.A)

    # flaand.f_la_and(person)

    and_triples_out = FunctionDependentPreprocessing_pb2.ANDTriples()

    and_triples = FunctionDependentPreprocessing_pb2.ANDTriples()
    for i in range(l_dash):
        and_triple = and_triples.triples.add()
        and_triple.id = i
        flaand.f_la_and(communicator, person, and_triple)

    # ****step_1****
    for i in range(l_dash):
        all_objects.append(i)

    # ****step_2****
    # partition objects random in buckets
    all_buckets = []
    for bucket in range(buckets):
        temporary_list = []
        for object in range(objects_per_bucket):
            temporary_list.append(all_objects.pop(randint(0, len(all_objects) - 1)))
        all_buckets.append(temporary_list)

    # print(all_buckets)

    for bucket in range(buckets):
        and_triple_out = and_triples_out.triples.add()
        for object in range(1, objects_per_bucket):
            if object == 1:
                old = all_buckets[bucket][object - 1]
            current = all_buckets[bucket][object]

            print(old, current)
            old = combine_two_leaky_and(old, current)

        print(all_buckets[bucket])

        pass

    # TODO how can i ensure to have corresponding key,mac,bit??
    '''
    for bucket in range(buckets):
        for object in range(objects_per_bucket):
            #print(all_buckets[bucket][object])
            pass
        pass
    '''

    # ****step_3****
    return and_triples_out


def combine_two_leaky_and(old, current):
    return current


f_a_and(Person(Person.A))
