from tools.gate import *
from tools.person import Person


def create_example_circuit_0(person: Person):
    and0 = AND(10, person, None, None)
    and1 = AND(20, person, None, None)
    xor3 = XOR(30, person, and0, and1)

    person.inputs = [10, 20] if person.x == Person.A else [11, 21]
    person.other_inputs = [11, 21] if person.x == Person.A else [10, 20]

    inputs = {10: and0, 20: and1}
    outputs = [xor3]
    num_and = 2
    return inputs, outputs, num_and


def create_example_circuit_1(person: Person):
    xor0 = XOR(10, person, None, None)
    xor1 = XOR(20, person, None, None)
    xor3 = XOR(30, person, xor0, xor1)

    person.inputs = [10, 20] if person.x == Person.A else [11, 21]
    person.other_inputs = [11, 21] if person.x == Person.A else [10, 20]

    inputs = {10: xor0, 20: xor1}
    outputs = [xor3]
    num_and = 0
    return inputs, outputs, num_and


def create_example_circuit_2(person: Person):
    and0 = AND(0, person, None, None)
    and1 = AND(10, person, None, None)
    xor2 = XOR(20, person, None, and0)
    xor3 = XOR(30, person, None, None)
    and4 = AND(40, person, None, xor3)
    and5 = AND(50, person, and0, and1)
    xor6 = XOR(60, person, and0, and4)
    and7 = AND(70, person, and5, xor6)
    xor8 = XOR(80, person, xor2, xor6)
    and9 = AND(90, person, xor3, and4)

    person.inputs = [0, 10, 20, 30] if person.x == Person.A else [1, 11, 31, 40]
    person.other_inputs = [1, 11, 31, 40] if person.x == Person.A else [0, 10, 20, 30]

    inputs = {0: and0, 10: and1, 20: xor2, 30: xor3, 40: and4}
    outputs = [and7, xor8, and9]
    num_and = 6
    return inputs, outputs, num_and


def create_example_circuit_3(person: Person):
    and0 = AND(10, person, None, None)
    and1 = AND(20, person, None, None)
    and3 = AND(30, person, and0, and1)

    person.inputs = [10, 20] if person.x == Person.A else [11, 21]
    person.other_inputs = [11, 21] if person.x == Person.A else [10, 20]

    inputs = {10: and0, 20: and1}
    outputs = [and3]
    num_and = 3
    return inputs, outputs, num_and


def create_example_circuit_4(person: Person):
    and0 = AND(10, person, None, None, True)
    and1 = AND(20, person, None, None, True)
    and3 = AND(30, person, None, None)
    and4 = AND(40, person, and1, and3, True)
    xor5 = XOR(50, person, and3, and4)
    xor6 = XOR(60, person, and0, and4)
    and7 = AND(70, person, xor5, xor6, True)
    and8 = AND(80, person, xor5, xor6, True)
    and9 = AND(90, person, and7, and8)
    and10 = AND(100, person, xor5, and3, True)

    person.inputs = [10, 20, 30] if person.x == Person.A else [11, 21, 31]
    person.other_inputs = [11, 21, 31] if person.x == Person.A else [10, 20, 30]

    inputs = {10: and0, 20: and1, 30: and3}
    outputs = [and9, and10]
    num_and = 8
    return inputs, outputs, num_and


def create_example_circuit_5(person: Person):
    and0 = AND(10, person, None, None, True)
    and1 = AND(20, person, None, None, True)
    and3 = AND(30, person, and0, and1)

    person.inputs = [10, 20] if person.x == Person.A else [11, 21]
    person.other_inputs = [11, 21] if person.x == Person.A else [10, 20]

    inputs = {10: and0, 20: and1}
    outputs = [and3]
    num_and = 3
    return inputs, outputs, num_and


def create_and_gate(person: Person):
    and0 = AND(10, person, None, None)

    person.inputs = [10] if person.x == Person.A else [11]
    person.other_inputs = [11] if person.x == Person.A else [10]

    inputs = {10: and0}
    outputs = [and0]
    num_and = 1
    return inputs, outputs, num_and


def create_xor_gate(person: Person):
    xor0 = XOR(10, person, None, None)

    person.inputs = [10] if person.x == Person.A else [11]
    person.other_inputs = [11] if person.x == Person.A else [10]

    inputs = {10: xor0}
    outputs = [xor0]
    num_and = 0
    return inputs, outputs, num_and


def create_nand_gate(person: Person):
    and0 = AND(10, person, None, None, True)

    person.inputs = [10] if person.x == Person.A else [11]
    person.other_inputs = [11] if person.x == Person.A else [10]

    inputs = {10: and0}
    outputs = [and0]
    num_and = 1
    return inputs, outputs, num_and


def and_operation(person: Person):
    """
    Circuit for an 8 bit and operation of two integers.
    :param person:
    """
    and0 = []
    inputs = {}
    for i in range(8):
        and0.append(AND(i * 10, person, None, None))
        inputs[i * 10] = and0[i]

    person.inputs = [0, 10, 20, 30, 40, 50, 60, 70] if person.x == Person.A else [1, 11, 21, 31, 41, 51, 61, 71]
    person.other_inputs = [1, 11, 21, 31, 41, 51, 61, 71] if person.x == Person.A else [0, 10, 20, 30, 40, 50, 60, 70]

    num_and = 8
    return inputs, and0, num_and
