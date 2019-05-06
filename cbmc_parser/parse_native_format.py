import csv
import os
from cbmc_parser.gate_helper import GateHelper

# ------------------------------ functions for getting file contents ------------------------------

def get_nonio_gate_file(folder_name):
    """
    Get file object for output.gate.txt

    :param folder_name: folder which contains output.* files for a circuit
    :return: file object for output.gate.txt from specified folder
    """

    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, 'gate_files', folder_name, 'output.gate.txt')
    return open(abs_file_path, 'r', newline='', encoding="utf8")


def get_input_gate_file(folder_name):
    """
    Get file object for output.inputs.txt

    :param folder_name: folder which contains output.* files for a circuit
    :return: file object for output.inputs.txt from specified folder
    """

    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, 'gate_files', folder_name, 'output.inputs.txt')
    return open(abs_file_path, 'r', newline='', encoding="utf8")


def get_partyA_input_range_file(folder_name):
    """
    Get file object for output.inputs.partyA.txt

    :param folder_name: folder which contains output.* files for a circuit
    :return: file object for output.inputs.partyA.txt from specified folder
    """

    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, 'gate_files', folder_name, 'output.inputs.partyA.txt')
    return open(abs_file_path, 'r', newline='', encoding="utf8")


def get_partyB_input_range_file(folder_name):
    """
    Get file object for output.inputs.partyB.txt

    :param folder_name: folder which contains output.* files for a circuit
    :return: file object for output.inputs.partyB.txt from specified folder
    """

    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, 'gate_files', folder_name, 'output.inputs.partyB.txt')
    return open(abs_file_path, 'r', newline='', encoding="utf8")


def get_input_mapping_file(folder_name):
    """
    Get file object for output.mapping.txt

    :param folder_name: folder which contains output.* files for a circuit
    :return: file object for output.mapping.txt from specified folder
    """

    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, 'gate_files', folder_name, 'output.mapping.txt')
    return open(abs_file_path, 'r', newline='', encoding="utf8")

# -------------------------------------------------------------------------------------------------

def get_inputrange_partyA(partyA_inputrange_file, max_input_id):
    """
    Get input ranges for all inputs of partyA

    :param folder_name: file object of output.inputs.partyA.txt file
    :return: list of tuples (x,y), where x is position the first bit of the integer and y the position of the last bit
    """

    reader_inputrange_partyA = csv.reader(partyA_inputrange_file, delimiter=' ', quoting=csv.QUOTE_NONE)
    line = next(reader_inputrange_partyA, None)
    result = []
    while line:
        result.append((int(line[1]), int(line[1]) - 1 + int(line[2])))
        line = next(reader_inputrange_partyA, None)
    partyA_inputrange_file.close()
    return result


def get_inputrange_partyB(partyB_inputrange_file, max_input_id):
    """
    Get input ranges for all inputs of partyB

    :param folder_name: file object of output.inputs.partyB.txt file
    :return: list of tuples (x,y), where x is position the first bit of the integer and y the position of the last bit
    """
    reader_inputrange_partyB = csv.reader(partyB_inputrange_file, delimiter=' ', quoting=csv.QUOTE_NONE)
    line = next(reader_inputrange_partyB, None)
    result = []
    while line:
        result.append((int(line[1]), int(line[1]) - 1 + int(line[2])))
        line = next(reader_inputrange_partyB, None)
    partyB_inputrange_file.close()
    return result



def transform_wire_string_to_tuple(wirestring):
    """
    Transforms String representation to integer

    :param wirestring: String configuration which occurs in output.gate.txt and output.inputs.txt file
    :return: decomposition of the String into Tuple of three Integers
    """

    wirelist = wirestring.split(':')
    return int(wirelist[0]), int(wirelist[1]), int(wirelist[2])


def get_input_gates(input_gate_file):
    """
    Parse input_gate_file file object and convert contents to list of GateHelper objects

    :param input_gate_file: file object of output.inputs.txt file
    :return: list containing GateHelper objects representing the gates parsed from input_gate_file
    """

    reader_input_gates = csv.reader(input_gate_file, delimiter=' ', quoting=csv.QUOTE_NONE)

    input_gate_list = []

    for gate in reader_input_gates:
        gateid = int(gate[0][8:])
        gatetype = 'INPUT'
        num_of_inputs = 0
        output_to = []
        is_circuit_output = False
        output_id_list = []
        for output_wire in gate[1:]:
            (_, gateid_out, inputid_out) = transform_wire_string_to_tuple(output_wire)
            if gateid_out < 0:
                is_circuit_output = True
                output_id_list.append(gateid_out)
            output_to.append((gateid_out, inputid_out))

        input_gate_object = GateHelper(gateid, gatetype, num_of_inputs, output_to, is_circuit_output,
                                       output_id_list)
        input_gate_list.append(input_gate_object)

    input_gate_file.close()
    return input_gate_list


def get_nonio_gates(nonio_gate_file):
    """
    Parse nonio_gate_file file object and convert contents to list of GateHelper objects

    :param input_gate_file: file object of output.gate.txt file
    :return: list containing GateHelper objects representing the gates parsed from nonio_gate_file
    """

    reader_nonio_gates = csv.reader(nonio_gate_file, delimiter=' ', quoting=csv.QUOTE_NONE)

    nonio_gate_list = []
    current_id = 1

    for gate in reader_nonio_gates:
        gateid = current_id
        gatetype = gate[0]
        num_of_inputs = gate[1]
        output_to = []
        is_circuit_output = False
        output_id_list = []
        for output_wire in gate[2:]:
            (_, gateid_out, inputid_out) = transform_wire_string_to_tuple(output_wire)
            if gateid_out < 0:
                is_circuit_output = True
                output_id_list.append(gateid_out)
            output_to.append((gateid_out, inputid_out))

        nonio_gate_object = GateHelper(gateid, gatetype, num_of_inputs, output_to, is_circuit_output,
                                       output_id_list)
        nonio_gate_list.append(nonio_gate_object)
        current_id += 1

    nonio_gate_file.close()
    return nonio_gate_list


def parse_native(output_file):
    """
    Takes ranges and an output file as input, parses files and generates representation of circuit

    Output files have to contain output.gate.txt, output.inputs.partyA.txt, output.inputs.partyB.txt,
    output.inputs.txt and output.mapping.txt

    Output files are generated by CBMC-GC ANSI-C parser: https://gitlab.com/securityengineering/CBMC-GC-2.git

    Note that the index of a gate in a list is equal to its id - 1 since there is no gate-id 0

    :param output_file: string with path to folder that contains output files of cmbc
    :return following
        input_gate_list: list of input gates(of class GateHelper with self.type = INPUT):
            they output a constant value specified by the input of the circuit
        rangeA: the range of input-gate-ids which correspond to input of A
        rangeB: the range of input-gate-ids which correspond to input of B
        nonio_gate_list: list containing all gates(of class gate helper with self.type = XOR, AND, NOT, OR)
            except the input gates
    """

    # get informations on the input from output files
    input_gate_list = get_input_gates(get_input_gate_file(output_file))
    num_of_input_gates = len(input_gate_list)
    rangeA = get_inputrange_partyA(get_partyA_input_range_file(output_file), num_of_input_gates)
    rangeB = get_inputrange_partyB(get_partyB_input_range_file(output_file), num_of_input_gates)

    # get information on nonio gates
    nonio_gate_list = get_nonio_gates(get_nonio_gate_file(output_file))

    return input_gate_list, rangeA, rangeB, nonio_gate_list
