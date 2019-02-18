import csv


def get_nonio_gate_file(folder_name):
    return open('gate_files/' + folder_name + '/output.gate.txt', 'r', newline='', encoding="utf8")


def get_input_gate_file(folder_name):
    return open('gate_files/' + folder_name + '/output.inputs.txt', 'r', newline='', encoding="utf8")


def get_partyA_input_range_file(folder_name):
    return open('gate_files/' + folder_name + '/output.inputs.partyA.txt', 'r', newline='', encoding="utf8")


def get_partyB_input_range_file(folder_name):
    return open('gate_files/' + folder_name + '/output.inputs.partyB.txt', 'r', newline='', encoding="utf8")


def get_input_mapping_file(folder_name):
    return open('gate_files/' + folder_name + '/output.mapping.txt', 'r', newline='', encoding="utf8")



def parse_native(partyA_input_range, partyB_input_range, input_gates, nonio_gates):
    """
    Takes ranges and .output files as input, parses files and generates representation of circuit

    :param partyA_input_range:
    :param partyB_input_range:
    :param input_gates:
    :param nonio_gates:
    :return:
    """

    reader_input_gates = csv.reader(input_gates, delimiter=' ', quoting=csv.QUOTE_NONE)
    reader_nonio_gates = csv.reader(nonio_gates, delimiter=' ', quoting=csv.QUOTE_NONE)
