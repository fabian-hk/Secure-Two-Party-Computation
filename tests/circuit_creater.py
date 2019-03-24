from tools.gate import *
from tools.person import Person


def create_example_circuit_0(person: Person):
    and0 = AND(10, person, None, None)
    and1 = AND(20, person, None, None)
    xor3 = XOR(30, person, and0, and1)

    person.inputs = [10, 20] if person.x == Person.A else [11, 21]
    person.other_inputs = [11, 21] if person.x == Person.A else [10, 20]

    inputs = [and0, and1]
    outputs = [xor3]
    return inputs, outputs


def create_example_circuit_1(person: Person):
    xor0 = XOR(10, person, None, None)
    xor1 = XOR(20, person, None, None)
    xor3 = XOR(30, person, xor0, xor1)

    person.inputs = [10, 20] if person.x == Person.A else [11, 21]
    person.other_inputs = [11, 21] if person.x == Person.A else [10, 20]

    inputs = [xor0, xor1]
    outputs = [xor3]
    return inputs, outputs


def create_example_circuit_2(person: Person):
    and0 = AND(10, person, None, None)

    person.inputs = [10] if person.x == Person.A else [11]
    person.other_inputs = [11] if person.x == Person.A else [10]

    inputs = [and0]
    outputs = [and0]
    return inputs, outputs
