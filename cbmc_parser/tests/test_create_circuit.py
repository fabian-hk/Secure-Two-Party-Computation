import unittest

from cbmc_parser.gate_helper import GateHelper
from cbmc_parser.create_circuit import create_circuit_from_output_data
from tools.person import Person
from tools.gate import Gate
from tests.plain_evaluator import plain_circuit_evaluation


class TestCreateCircuit1(unittest.TestCase):

    def printgate(self, gate):
        prea = 'None'
        preb = 'None'
        if gate.pre_a is not None:
            prea = gate.pre_a.id
        if gate.pre_b is not None:
            preb = gate.pre_b.id
        type = 'None'
        if gate.type == Gate.TYPE_XOR:
            type = 'XOR'
        if gate.type == Gate.TYPE_AND:
            if gate.is_nand:
                type = 'NAND'
            else:
                type = 'AND'

        print('gate-id: ' + str(gate.id) + '  gate-type: ' + type + '  pre_a: ' + str(
            prea) + '  pre_b: ' + str(preb))

    def test_read_output_1(self):
        personA = Person(Person.A)
        inputs, outputs, num_and, gatelist = create_circuit_from_output_data('test_output_1', personA, True)
        print('-------inputs-------')
        for key in inputs.keys():
            print('input-object-id: ' + str(key) + '  input-object-id: ' + str(inputs[key].id))
        print('-------outputs-------')
        for gate in outputs:
            TestCreateCircuit1.printgate(self, gate)
        print('-------num_and-------')
        print(num_and)
        print('-------gatelist-------')
        for gate in gatelist:
            TestCreateCircuit1.printgate(self, gate)

    def test_gatelist_1(self):
        personA = Person(Person.A)
        inputs, outputs, num_and, gatelist = create_circuit_from_output_data('test_output_1', personA, True)

        # test if number of gates of specific types is correct
        num_type_and = 0
        num_type_xor = 0
        num_type_nand = 0
        for gate in gatelist:

            if gate.type == Gate.TYPE_XOR:
                num_type_xor += 1
            if gate.type == Gate.TYPE_AND:
                if gate.is_nand:
                    num_type_nand += 1
                else:
                    num_type_and += 1

        print("num_and: " + str(num_type_and))
        print("num_nand: " + str(num_type_nand))
        print("num_xor: " + str(num_type_xor))
        self.assertEqual(num_type_and + num_type_xor + num_type_nand, len(gatelist))
        self.assertEqual(7, len(gatelist))
        self.assertEqual(2, num_type_and)
        self.assertEqual(4, num_type_nand)
        self.assertEqual(1, num_type_xor)

        # test if ids always increase by 10
        old_id = gatelist[0].id
        for i in range(1, len(gatelist)):
            self.assertEqual(old_id + 10, gatelist[i].id)
            old_id = gatelist[i].id

        # test if last gate has correct id
        self.assertEqual(len(gatelist) * 10, gatelist[len(gatelist) - 1].id)

    def test_create_circuit_num_and_1(self):
        personA = Person(Person.A)
        inputs, outputs, num_and = create_circuit_from_output_data("test_output_1", personA)
        self.assertEqual(6, num_and)

    def test_create_circuit_inputs_1(self):
        personA = Person(Person.A)
        inputs, outputs, num_and = create_circuit_from_output_data("test_output_1", personA)

        self.assertEqual(3, len(inputs.keys()))
        self.assertEqual(10,inputs[10].id)
        self.assertEqual(20, inputs[20].id)
        self.assertEqual(40, inputs[40].id)

    def test_person_list(self):
        personA = Person(Person.A)
        inputs, outputs, num_and = create_circuit_from_output_data("test_output_1", personA)

    def test_execute_circuit_1(self):
        #in_vals_a = ["10"]
        in_vals_a = [1]
        #in_vals_b = ["01"]
        in_vals_b = [1]

        person_a = Person(Person.A)
        _, outputs, _ = create_circuit_from_output_data("test_output_1", person_a)
        #person_a.load_input_string(in_vals_a)
        person_a.load_input_integer(in_vals_a)
        person_b = Person(Person.B)
        _, outputs, _ = create_circuit_from_output_data("test_output_1", person_b)
        #person_b.load_input_string(in_vals_b)
        person_b.load_input_integer(in_vals_b)
        in_vals = person_a.in_vals
        in_vals.update(person_b.in_vals)

        x = plain_circuit_evaluation(outputs, in_vals)
        self.assertEquals(x[50][0], 1)



class TestCreateCircuit2(unittest.TestCase):
    def printgate(self, gate):
        prea = 'None'
        preb = 'None'
        if gate.pre_a is not None:
            prea = gate.pre_a.id
        if gate.pre_b is not None:
            preb = gate.pre_b.id
        type = 'None'
        if gate.type == Gate.TYPE_XOR:
            type = 'XOR'
        if gate.type == Gate.TYPE_AND:
            if gate.is_nand:
                type = 'NAND'
            else:
                type = 'AND'

        print('gate-id: ' + str(gate.id) + '  gate-type: ' + type + '  pre_a: ' + str(
            prea) + '  pre_b: ' + str(preb))

    def test_read_output_2(self):
        personA = Person(Person.A)
        inputs, outputs, num_and, gatelist = create_circuit_from_output_data('test_output_2', personA, True)
        print('-------inputs-------')
        for key in inputs.keys():
            print('input-object-id: ' + str(key) + '  input-object-id: ' + str(inputs[key].id))
        print('-------outputs-------')
        for gate in outputs:
            TestCreateCircuit1.printgate(self, gate)
        print('-------num_and-------')
        print(num_and)
        print('-------gatelist-------')
        for gate in gatelist:
            TestCreateCircuit1.printgate(self, gate)

    def test_create_circuit_num_and_2(self):
        personA = Person(Person.A)
        inputs, outputs, num_and = create_circuit_from_output_data("test_output_2", personA)
        self.assertEqual(1, num_and)

    def test_create_circuit_inputs_2(self):
        personA = Person(Person.A)
        inputs, outputs, num_and = create_circuit_from_output_data("test_output_2", personA)

        self.assertEqual(1, len(inputs.keys()))

    def test_gatelist_2(self):
        personA = Person(Person.A)
        inputs, outputs, num_and, gatelist = create_circuit_from_output_data("test_output_2", personA, True)

        self.assertEqual(10, gatelist[0].id)
        self.assertEqual(None, gatelist[0].pre_a)
        self.assertEqual(None, gatelist[0].pre_b)
        self.assertEqual(Gate.TYPE_AND, gatelist[0].type)
        self.assertEqual(False, gatelist[0].is_nand)

        num_type_and = 0
        num_type_xor = 0
        num_type_nand = 0
        for gate in gatelist:
            if gate.type == Gate.TYPE_XOR:
                num_type_xor += 1
            if gate.type == Gate.TYPE_AND:
                if gate.is_nand:
                    num_type_nand += 1
                else:
                    num_type_and += 1

        print("num_and: " + str(num_type_and))
        print("num_nand: " + str(num_type_nand))
        print("num_xor: " + str(num_type_xor))
        self.assertEqual(1, num_type_and)
        self.assertEqual(0, num_type_nand)
        self.assertEqual(0, num_type_xor)


if __name__ == '__main__':
    unittest.main()
