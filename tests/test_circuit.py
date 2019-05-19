import unittest
from random import randint, random
import numpy as np

from tests.test_circuit_creater import *
from tests.evaluate_circuit import evaluate_circuit
from tests.plain_evaluator import *
from tools.person import Person


class TestCircuit(unittest.TestCase):

    def test_circuit_0(self):
        for i in range(4):
            in_vals_a = [str(randint(0, 1)) + str(randint(0, 1))]
            in_vals_b = [str(randint(0, 1)) + str(randint(0, 1))]

            res_mpc, res_plain = evaluate_circuit(create_example_circuit_0, in_vals_a, in_vals_b)

            # check if the MPC and plain result are the same
            self.assertEqual(res_mpc, res_plain)

    def test_circuit_1(self):
        for i in range(4):
            in_vals_a = [str(randint(0, 1)) + str(randint(0, 1))]
            in_vals_b = [str(randint(0, 1)) + str(randint(0, 1))]

            res_mpc, res_plain = evaluate_circuit(create_example_circuit_1, in_vals_a, in_vals_b)

            # check if the MPC and plain result are the same
            self.assertEqual(res_mpc, res_plain)

    def test_circuit_2(self):
        for i in range(4):
            in_vals_a = [str(randint(0, 1)) + str(randint(0, 1)) + str(randint(0, 1)) + str(randint(0, 1))]
            in_vals_b = [str(randint(0, 1)) + str(randint(0, 1)) + str(randint(0, 1)) + str(randint(0, 1))]

            res_mpc, res_plain = evaluate_circuit(create_example_circuit_2, in_vals_a, in_vals_b)

            # check if the MPC and plain result are the same
            self.assertEqual(res_mpc, res_plain)

    def test_circuit_3(self):
        for i in range(4):
            in_vals_a = [str(randint(0, 1)) + str(randint(0, 1))]
            in_vals_b = [str(randint(0, 1)) + str(randint(0, 1))]

            res_mpc, res_plain = evaluate_circuit(create_example_circuit_3, in_vals_a, in_vals_b)

            # check if the MPC and plain result are the same
            self.assertEqual(res_mpc, res_plain)

    def test_circuit_4(self):
        for i in range(4):
            in_vals_a = [str(randint(0, 1)) + str(randint(0, 1)) + str(randint(0, 1))]
            in_vals_b = [str(randint(0, 1)) + str(randint(0, 1)) + str(randint(0, 1))]

            res_mpc, res_plain = evaluate_circuit(create_example_circuit_4, in_vals_a, in_vals_b)

            # check if the MPC and plain result are the same
            self.assertEqual(res_mpc, res_plain)

    def test_circuit_5(self):
        for i in range(4):
            in_vals_a = [str(randint(0, 1)) + str(randint(0, 1))]
            in_vals_b = [str(randint(0, 1)) + str(randint(0, 1))]

            res_mpc, res_plain = evaluate_circuit(create_example_circuit_5, in_vals_a, in_vals_b)

            # check if the MPC and plain result are the same
            self.assertEqual(res_mpc, res_plain)

    def test_and_operation(self):
        for i in range(4):
            in_vals_a = [str(randint(0, 1)) + str(randint(0, 1)) + str(randint(0, 1)) + str(randint(0, 1)) + str(
                randint(0, 1)) + str(randint(0, 1)) + str(randint(0, 1)) + str(randint(0, 1))]
            in_vals_b = [str(randint(0, 1)) + str(randint(0, 1)) + str(randint(0, 1)) + str(randint(0, 1)) + str(
                randint(0, 1)) + str(randint(0, 1)) + str(randint(0, 1)) + str(randint(0, 1))]

            res_mpc, res_plain = evaluate_circuit(and_operation, in_vals_a, in_vals_b)

            # check if the MPC and plain result are the same
            self.assertEqual(res_mpc, res_plain)


class TestFunctions(unittest.TestCase):

    def test_add(self):
        for i in range(5):
            in_vals_a = [randint(0, 1073741823)]
            in_vals_b = [randint(0, 1073741823)]

            if random() < 0.5:
                in_vals_a[0] *= -1

            if random() < 0.5:
                in_vals_b[0] *= -1

            res_mpc_proto, res_mpc, res_plain = evaluate_circuit("add", in_vals_a, in_vals_b, True)

            # check if the MPC and plain result are the same
            self.assertEqual(res_mpc, res_plain)
            res_dez = h.print_output(res_mpc_proto)
            self.assertEqual(res_dez, (in_vals_a[0] + in_vals_b[0]))

    def test_equality_test(self):
        for i in range(5):
            in_vals_a = [randint(0, 4294967295)]
            if random() < 0.75:
                in_vals_b = in_vals_a
            else:
                in_vals_b = [randint(0, 4294967295)]

            res_mpc_proto, res_mpc, res_plain = evaluate_circuit("equality_test", in_vals_a, in_vals_b, True)

            # check if the MPC and plain result are the same
            self.assertEqual(res_mpc, res_plain)
            res_dez = h.print_output(res_mpc_proto)
            self.assertEqual(res_dez == 1, in_vals_a == in_vals_b)

    def test_mean(self):
        for i in range(5):
            in_vals_a = [randint(0, 268435454), randint(0, 268435454), randint(0, 268435454), randint(0, 268435454)]
            in_vals_b = [randint(0, 268435454), randint(0, 268435454), randint(0, 268435454), randint(0, 268435454)]

            res_mpc_proto, res_mpc, res_plain = evaluate_circuit("mean", in_vals_a, in_vals_b, True)

            # check if the MPC and plain result are the same
            self.assertEqual(res_mpc, res_plain)
            res_dez = h.print_output(res_mpc_proto)
            self.assertEqual(int(np.mean(in_vals_a + in_vals_b)), res_dez)


class TestGates(unittest.TestCase):

    def test_and_gate(self):
        in_vals_a = ["0", "1"]
        in_vals_b = ["0", "1"]

        for i in range(4):
            for in_val_a in in_vals_a:
                for in_val_b in in_vals_b:
                    res_mpc, res_plain = evaluate_circuit(create_and_gate, in_val_a, in_val_b)

                    # check if the MPC and plain result are the same
                    self.assertEqual(res_mpc, res_plain)

    def test_xor_gate(self):
        in_vals_a = ["0", "1"]
        in_vals_b = ["0", "1"]

        for i in range(4):
            for in_val_a in in_vals_a:
                for in_val_b in in_vals_b:
                    res_mpc, res_plain = evaluate_circuit(create_xor_gate, in_val_a, in_val_b)

                    # check if the MPC and plain result are the same
                    self.assertEqual(res_mpc, res_plain)

    def test_nand_gate(self):
        in_vals_a = ["0", "1"]
        in_vals_b = ["0", "1"]

        for i in range(4):
            for in_val_a in in_vals_a:
                for in_val_b in in_vals_b:
                    res_mpc, res_plain = evaluate_circuit(create_nand_gate, in_val_a, in_val_b)

                    # check if the MPC and plain result are the same
                    self.assertEqual(res_mpc, res_plain)
