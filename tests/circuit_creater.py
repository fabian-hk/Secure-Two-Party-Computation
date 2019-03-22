from tools.gate import *
from tools.person import Person


def create_example_circuit_0(person: Person):
    and0 = AND(10, person, None, None)
    and1 = AND(20, person, None, None)
    xor3 = XOR(30, person, and0, and1)
    inputs = [and0, and1]
    outputs = [xor3]
    return inputs, outputs


def create_example_circuit_1(person: Person):
    xor0 = XOR(10, person, None, None)
    xor1 = XOR(20, person, None, None)
    xor3 = XOR(30, person, xor0, xor1)
    inputs = [xor0, xor1]
    outputs = [xor3]
    return inputs, outputs
