from tools.gate import *
from tools.person import Person
import parse_native_format as pnf
from gate_helper import GateHelper


def create_circuit_from_output_data(output_file, person: Person):
    """

    :param output_file: file that contains cbmc outputs
    :param person:
    :type person: Person
    :return: inputs, outputs
    """
    input_gate_list, rangeA, rangeB, nonio_gate_list = pnf.parse_native(output_file)

    mark_as_not = Gate(-1, person, None, None)
    mark_as_or = Gate(0, person, None, None)

    #list containing the Gate ojects
    gatelist = []
    output_mapping = {}

    # turn all GateHelper objects into Gate objects, fill output_mapping
    for gate in nonio_gate_list:
        if gate.type == "AND":
            gatelist.append(AND(gate.id * 10, person, None, None))
        elif gate.type == "XOR":
            gatelist.append(XOR(gate.id * 10, person, None, None))
        elif gate.type == "NAND":
            gatelist.append(AND(gate.id * 10, person, None, None, True))
        elif gate.type == "NOT":
            gatelist.append(AND(gate.id * 10, person, mark_as_not, None, True))
        elif gate.type == "OR":
            gatelist.append(AND(gate.id * 10, person, mark_as_or, mark_as_or, True))

        if gate.is_circuit_output:
            print(gate.id)
            for bit_number in gate.output_number_list:
                output_mapping[-bit_number] = gate.id

    #connect all nonio gates
    for gate_from in nonio_gate_list:
        for gate_to in gate.output_to:

            gate_to_update = gatelist[gate_to[0] - 1]
            gate_to_fill_in = gatelist[gate_from.id - 1]

            if gate_to_update.pre_a == mark_as_not:
                gate_to_update.pre_a = gate_to_fill_in
                gate_to_update.pre_b = gate_to_fill_in
                gate_to_fill_in.next.append((gate_to_update, Gate.WIRE_A))
                gate_to_fill_in.next.append((gate_to_update, Gate.WIRE_B))

            elif gate_to[1] == 0:
                if gate_to_update.pre_a == mark_as_or:
                    new_not = AND(len(gatelist) * 10, person, gate_to_fill_in, gate_to_fill_in, True)
                    new_not.next.append((gate_to_update, Gate.WIRE_A))
                    gatelist.append(new_not)
                    gate_to_update.pre_a = new_not
                else:
                    gate_to_update.pre_a = gate_to_fill_in
                    gate_to_fill_in.next.append((gate_to_update, Gate.WIRE_A))

            elif gate_to[1] == 1:
                if gate_to_update.pre_b == mark_as_or:
                    new_not = AND(len(gatelist) * 10, person, gate_to_fill_in, gate_to_fill_in, True)
                    new_not.next.append((gate_to_update, Gate.WIRE_B))
                    gatelist.append(new_not)
                    gate_to_update.pre_b = new_not
                else:
                    gate_to_update.pre_b = gate_to_fill_in
                    gate_to_fill_in.next.append((gate_to_update, Gate.WIRE_B))

    for i in output_mapping.keys():
        print(str(i) + "---" + str(output_mapping[i]))

    print(rangeA)
    print(rangeB)
    #connect inputs to gates
    #TODO connect inputs
    for gate_from in input_gate_list:
        for gate_to in gate.output_to:
            #gate_to_update = gatelist[gate_to[0] - 1]
            pass




create_circuit_from_output_data("eucl_dist_output", None)
