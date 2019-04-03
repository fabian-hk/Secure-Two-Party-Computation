import unittest

from cbmc_parser.gate_helper import GateHelper
from cbmc_parser.parse_native_format import parse_native


class TestParseCircuit1(unittest.TestCase):
    def test_parse_native_ranges_1(self):
        input_gate_list, rangeA, rangeB, nonio_gate_list = parse_native("test_output_1")
        self.assertEqual((1,2),rangeA)
        self.assertEqual((3,4),rangeB)

    def test_parse_native_input_gate_list_1(self):
        input_gate_list, rangeA, rangeB, nonio_gate_list = parse_native("test_output_1")
        self.assertEqual(4,len(input_gate_list))

        self.assertEqual(2,input_gate_list[1].id)
        self.assertEqual(4, input_gate_list[3].id)

        self.assertEqual(1,input_gate_list[2].output_to[0][0])
        self.assertEqual(1, input_gate_list[2].output_to[0][0])
        self.assertEqual(4, input_gate_list[3].output_to[1][0])

        self.assertEqual('INPUT',input_gate_list[0].type)

    def test_parse_native_nonio_gate_list_1(self):
        input_gate_list, rangeA, rangeB, nonio_gate_list = parse_native("test_output_1")
        self.assertEqual(5,len(nonio_gate_list))

        type_list = ['XOR','AND','OR','AND','NOT']
        for i in range(0,5):
            self.assertEqual(type_list[i],nonio_gate_list[i].type)

        for i in range(0,5):
            self.assertEqual(i+1,nonio_gate_list[i].id)

        output_list = [[(3,0)],[(3,1)],[(4,0)],[(5,0)],[(-1,0)]]
        for i in range(0,5):
            for j in range(0,len(output_list[i])):
                self.assertEqual(output_list[i][j],nonio_gate_list[i].output_to[j])

        self.assertFalse(nonio_gate_list[2].is_circuit_output)
        self.assertTrue(nonio_gate_list[4].is_circuit_output)

        self.assertEqual(-1,nonio_gate_list[4].output_number_list[0])
        self.assertEqual(1, len(nonio_gate_list[4].output_number_list))



class TestParseCircuit2(unittest.TestCase):
    def test_parse_native_ranges_2(self):
        input_gate_list, rangeA, rangeB, nonio_gate_list = parse_native("test_output_2")
        self.assertEqual(1, rangeA[0])
        self.assertEqual(1, rangeA[1])
        self.assertEqual(2, rangeB[0])
        self.assertEqual(2, rangeB[0])

    def test_parse_native_input_gate_list_2(self):
        input_gate_list, rangeA, rangeB, nonio_gate_list = parse_native("test_output_2")

        self.assertEqual(1, input_gate_list[0].id)
        self.assertEqual(2, input_gate_list[1].id)

        self.assertEqual(1, input_gate_list[0].output_to[0][0])
        self.assertEqual(0, input_gate_list[0].output_to[0][1])
        self.assertEqual(1, input_gate_list[1].output_to[0][0])
        self.assertEqual(1, input_gate_list[1].output_to[0][1])

        self.assertEqual(2, len(input_gate_list))

    def test_parse_native_nonio_gate_list_2(self):
        input_gate_list, rangeA, rangeB, nonio_gate_list = parse_native("test_output_2")

        self.assertEqual(1, nonio_gate_list[0].id)

        self.assertEqual(-1, nonio_gate_list[0].output_to[0][0])

        self.assertEqual(1, len(nonio_gate_list))

