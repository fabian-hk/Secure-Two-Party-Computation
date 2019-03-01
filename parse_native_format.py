import csv


class gate_helper:

    def __init__(self, id, type, num_of_inputs, output_to, is_circuit_output, output_number_list):
        self.id = id
        self.type = type
        self.num_of_inputs = num_of_inputs
        self.output_to = output_to
        self.output_value = None
        self.is_circuit_output = is_circuit_output
        self.output_number_list = output_number_list


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


def get_inputrange_partyA(partyA_inputrange_file, max_input_id):
    reader_inputrange_partyA = csv.reader(partyA_inputrange_file, delimiter=' ', quoting=csv.QUOTE_NONE)
    # TODO check if there are more lines when more variables are used as input
    line1 = next(reader_inputrange_partyA)
    return (int(line1[1]), int(line1[2]))


def get_inputrange_partyB(partyB_inputrange_file, max_input_id):
    reader_inputrange_partyA = csv.reader(partyB_inputrange_file, delimiter=' ', quoting=csv.QUOTE_NONE)
    # TODO check if there are more lines when more variables are used as input
    line1 = next(reader_inputrange_partyA)
    startid = int(line1[1])
    endid = int(line1[2])
    if endid < startid:
        endid = max_input_id
    return (startid, endid)


def transform_wire_string_to_tuple(wirestring):
    wirelist = wirestring.split(':')
    return int(wirelist[0]), int(wirelist[1]), int(wirelist[2])


def get_input_gates(input_gate_file):
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

        input_gate_object = gate_helper(gateid, gatetype, num_of_inputs, output_to, is_circuit_output,
                                        output_id_list)
        input_gate_list.append(input_gate_object)

    return input_gate_list


def get_nonio_gates(nonio_gate_file):
    reader_input_gates = csv.reader(nonio_gate_file, delimiter=' ', quoting=csv.QUOTE_NONE)

    nonio_gate_list = []
    current_id = 1

    for gate in reader_input_gates:
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

        nonio_gate_object = gate_helper(gateid, gatetype, num_of_inputs, output_to, is_circuit_output,
                                        output_id_list)
        nonio_gate_list.append(nonio_gate_object)
        current_id += 1
    return nonio_gate_list


def parse_native(output_file):
    """
    Takes ranges and .output files as input, parses files and generates representation of circuit

    Note that the index of a gate in a list is equal to its id - 1 since there is no gate-id 0

    cmbc gc repository reference:  CBMC-GC-2/src/circuit-utils/src/circuit.cpp

    :param partyA_input_range:
    :param partyB_input_range:
    :param input_gates:
    :param nonio_gates:
    :return:
    """

    # get informations on the input from output files
    input_gate_list = get_input_gates(get_input_gate_file(output_file))
    num_of_input_gates = len(input_gate_list)
    rangeA = get_inputrange_partyA(get_partyA_input_range_file(output_file), num_of_input_gates)
    rangeB = get_inputrange_partyB(get_partyB_input_range_file(output_file), num_of_input_gates)

    # get information on nonio gates
    nonio_gate_list = get_nonio_gates(get_nonio_gate_file(output_file))

    return input_gate_list, rangeA, rangeB, nonio_gate_list
