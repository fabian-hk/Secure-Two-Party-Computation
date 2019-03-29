from typing import List, Dict

from tools import helper as h
from tools.gate import *
from tools.person import Person
from tests.circuit_creater import *


def plain_circuit_evaluation(output_gates: List, inputs: Dict[int, int]):
    """
    Takes the output gates of a circuit as a list and the inputs as dict with {WIRE_ID: INPUT_VALUE}.
    :param output_gates:
    :param inputs:
    :return: Return a dict with {WIRE_ID, OUTPUT_VALUE}
    :rtype Dict[int, bytes]
    """
    res = {}
    for out in output_gates:  # type: Gate
        stack = [-1]
        gate = out
        while stack:
            if not gate.a and gate.pre_a:
                stack.append(gate)
                gate = gate.pre_a
            elif not gate.b and gate.pre_b:
                stack.append(gate)
                gate = gate.pre_b
            elif not gate.evaluated:
                gate.evaluated = True
                if not gate.a:
                    gate.a = inputs[gate.id]
                if not gate.b:
                    gate.b = inputs[(gate.id + 1)]

                if gate.type == Gate.TYPE_XOR:
                    gate.y = h.xor(gate.a, gate.b)
                if gate.type == Gate.TYPE_AND:
                    gate.y = h.AND(gate.a, gate.b)
                    if gate.is_nand:
                        gate.y = h.xor(gate.y, b'\x01')

                for n in gate.next:  # type: tuple[Gate, int]
                    if n[1] == Gate.WIRE_A:
                        n[0].a = gate.y
                    elif n[1] == Gate.WIRE_B:
                        n[0].b = gate.y
                gate = stack.pop()

        print("Gate ID " + str(out.id) + " y: " + str(out.y))
        res[out.id] = out.y
    return res


if __name__ == "__main__":
    in_vals_a = "10"
    in_vals_b = "01"

    person_a = Person(Person.A)
    _, outputs, _ = create_example_circuit_5(person_a)
    person_a.load_input_string(in_vals_a)
    person_b = Person(Person.B)
    _, outputs, _ = create_example_circuit_5(person_b)
    person_b.load_input_string(in_vals_b)
    in_vals = person_a.in_vals
    in_vals.update(person_b.in_vals)

    print(plain_circuit_evaluation(outputs, in_vals))
