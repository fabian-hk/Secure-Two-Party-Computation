import unittest

from cbmc_parser.gate_helper import GateHelper
from cbmc_parser.create_circuit import create_circuit_from_output_data
from tools.person import Person
from tests.plain_evaluator import plain_circuit_evaluation


class TestCreateCircuit(unittest.TestCase):

    def test_output(self):
        personA = Person(Person.A)
        inputs, outputs, num_and = create_circuit_from_output_data("add_output",personA)
        print(inputs)
        print(outputs)
        print(num_and)

    def test_execute_circuit(self):
        in_vals_a = "10"
        in_vals_b = "01"

        person_a = Person(Person.A)
        _, outputs, _ = create_circuit_from_output_data("test_output", person_a)
        person_a.load_input_string(in_vals_a)
        person_b = Person(Person.B)
        _, outputs, _ = create_circuit_from_output_data("test_output", person_b)
        person_b.load_input_string(in_vals_b)
        in_vals = person_a.in_vals
        in_vals.update(person_b.in_vals)

        print(plain_circuit_evaluation(outputs, in_vals))
        self.assertTrue(1==1)


if __name__ == '__main__':
    unittest.main()