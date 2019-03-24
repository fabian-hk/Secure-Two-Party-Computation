import unittest

from tests.circuit_creater import *
from tests.evaluate_circuit import evaluate
from tests.plain_evaluator import *
from tools.person import Person


class TestCircuit(unittest.TestCase):

    def test_circuit_0(self):
        in_vals_a = "10"
        in_vals_b = "11"

        # do MPC
        res_dict_mpc = evaluate(create_example_circuit_0, in_vals_a, in_vals_b)

        # evaluate in plain form to check the output
        person_a = Person(Person.A)
        _, outputs = create_example_circuit_0(person_a)
        person_a.load_input_string(in_vals_a)
        person_b = Person(Person.B)
        _, outputs = create_example_circuit_0(person_b)
        person_b.load_input_string(in_vals_b)
        in_vals = person_a.in_vals
        in_vals.update(person_b.in_vals)
        res_dict_plain = plain_circuit_evaluation(outputs, in_vals)

        # check if the MPC and plain result are the same
        self.assertEqual(res_dict_mpc, res_dict_plain)

    def test_circuit_1(self):
        in_vals_a = "10"
        in_vals_b = "11"

        # do MPC
        res_dict_mpc = evaluate(create_example_circuit_1, in_vals_a, in_vals_b)

        # evaluate in plain form to check the output
        person_a = Person(Person.A)
        _, outputs = create_example_circuit_1(person_a)
        person_a.load_input_string(in_vals_a)
        person_b = Person(Person.B)
        _, outputs = create_example_circuit_1(person_b)
        person_b.load_input_string(in_vals_b)
        in_vals = person_a.in_vals
        in_vals.update(person_b.in_vals)
        res_dict_plain = plain_circuit_evaluation(outputs, in_vals)

        # check if the MPC and plain result are the same
        self.assertEqual(res_dict_mpc, res_dict_plain)
