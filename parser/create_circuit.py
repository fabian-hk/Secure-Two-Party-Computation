from tools.gate import *
from tools.person import Person
import parser.parse_native_format as pnf
from parser.gate_helper import GateHelper


def replace_not_by_nand(nonio_gate_list):
    """
    This will only work, if nonio_gate_list does not contain any nand gates

    :param nonio_gate_list: list of gate_helper objects that are no input gates
    :return: list of gates where all not-gates have been replaced by nand gates
    """
    for gate in nonio_gate_list:
        if gate.type == "NOT":
            gate.type = "NAND"
            gate.num_of_inputs = 2

        # duplicate all output_to entrys of ids of NOT and NAND Gates
        add_to_output_to = []
        for id in gate.output_to:
            if nonio_gate_list[id - 1].type == "NOT" or nonio_gate_list[id - 1].type == "NAND":
                add_to_output_to.append(id)
        gate.output_to += add_to_output_to

    return nonio_gate_list


def create_circuit_from_output_data(output_file, person: Person):
    input_gate_list, rangeA, rangeB, nonio_gate_list = pnf.parse_native(output_file)

    replace_not_by_nand(nonio_gate_list)

    print(nonio_gate_list)


create_circuit_from_output_data("parser/gate_files", None)
