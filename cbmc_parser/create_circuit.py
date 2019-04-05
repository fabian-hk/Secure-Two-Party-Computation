import os
import shutil

from tools.gate import *
from tools.person import Person
import cbmc_parser.parse_native_format as pnf
from cbmc_parser.gate_helper import GateHelper
import cbmc_parser.compile_ansic as compiler
from exceptions.CircuitCreationException import CircuitCreationError


def create_circuit_from_output_data(output_file, person: Person, test=False):
    """

    :param output_file: file that contains cbmc outputs
    :param person:
    :type person: Person
    :return: inputs, outputs
    """
    input_gate_list, rangeA, rangeB, nonio_gate_list = pnf.parse_native(output_file)

    # special gate for recognizing not gates
    mark_as_not = Gate(-1, person, None, None)
    # special gate for recognizing or gates
    mark_as_or = Gate(-2, person, None, None)

    # list containing the Gate objects
    gatelist = []
    # dictionary mapping output bits to gates
    output_mapping = {}

    # turn all GateHelper objects into Gate objects
    for gate in nonio_gate_list:
        if gate.type == "AND":
            gatelist.append(AND(gate.id * 10, person, None, None))
        elif gate.type == "XOR":
            gatelist.append(XOR(gate.id * 10, person, None, None))
        elif gate.type == "NOT":
            gatelist.append(AND(gate.id * 10, person, mark_as_not, None, True))
        elif gate.type == "OR":
            gatelist.append(AND(gate.id * 10, person, mark_as_or, mark_as_or, True))

    # fill output_mapping with outputs from nonio gates
    for gate in nonio_gate_list:
        if gate.is_circuit_output:
            for bit_number in gate.output_number_list:
                output_mapping[-bit_number] = gate.id

    # fill output_mapping with outputs from input gates
    for gate in input_gate_list:
        if gate.is_circuit_output:
            for bit_number in gate.output_number_list:
                output_mapping[-bit_number] = gate.id

    # connect all nonio Gate objects, expand gates marked as or and not to nands
    for gate_from in nonio_gate_list:
        for gate_to in gate_from.output_to:

            if gate_to[0] < 1:
                continue

            gate_to_update = gatelist[gate_to[0] - 1]
            gate_to_fill_in = gatelist[gate_from.id - 1]

            if gate_to_update.pre_a == mark_as_not:
                gate_to_update.pre_a = gate_to_fill_in
                gate_to_update.pre_b = gate_to_fill_in
                gate_to_fill_in.next.append((gate_to_update, Gate.WIRE_A))
                gate_to_fill_in.next.append((gate_to_update, Gate.WIRE_B))

            elif gate_to[1] == 0:
                if gate_to_update.pre_a == mark_as_or:
                    new_not = AND((len(gatelist) + 1) * 10, person, gate_to_fill_in, gate_to_fill_in, True)
                    new_not.next.append((gate_to_update, Gate.WIRE_A))
                    gatelist.append(new_not)
                    gate_to_update.pre_a = new_not
                else:
                    gate_to_update.pre_a = gate_to_fill_in
                    gate_to_fill_in.next.append((gate_to_update, Gate.WIRE_A))

            elif gate_to[1] == 1:
                if gate_to_update.pre_b == mark_as_or:
                    new_not = AND((len(gatelist) + 1) * 10, person, gate_to_fill_in, gate_to_fill_in, True)
                    new_not.next.append((gate_to_update, Gate.WIRE_B))
                    gatelist.append(new_not)
                    gate_to_update.pre_b = new_not
                else:
                    gate_to_update.pre_b = gate_to_fill_in
                    gate_to_fill_in.next.append((gate_to_update, Gate.WIRE_B))

    # fill inputs lists for both persons, expand gates marked as or and not to nands
    inputsA = []
    inputsB = []
    for i in range(rangeA[0], rangeA[1] + 1):
        inputsA.append([])
    for i in range(rangeB[0], rangeB[1] + 1):
        inputsB.append([])

    inputs = {}
    # connect inputs to gates and fill inputsA, inputsB, inputs dictionarys
    for gate_from in input_gate_list:
        for gate_to in gate_from.output_to:
            gate_to_update = gatelist[gate_to[0] - 1]

            if gate_to_update.pre_a == mark_as_not:
                gate_to_update.pre_a = None
                gate_to_update.pre_b = None

                inputs[gate_to_update.id] = gate_to_update
                if gate_from.id in range(rangeA[0], rangeA[1] + 1):
                    inputsA[gate_from.id - rangeA[0]].append(gate_to_update.id)
                    inputsA[gate_from.id - rangeA[0]].append(gate_to_update.id + 1)
                else:
                    inputsB[gate_from.id - rangeB[0]].append(gate_to_update.id)
                    inputsB[gate_from.id - rangeB[0]].append(gate_to_update.id + 1)

            elif gate_to[1] == 0:
                if gate_to_update.pre_a == mark_as_or:
                    new_not = AND((len(gatelist) + 1) * 10, person, None, None, True)
                    new_not.next.append((gate_to_update, Gate.WIRE_A))
                    gatelist.append(new_not)
                    gate_to_update.pre_a = new_not

                    inputs[new_not.id] = new_not
                    if gate_from.id in range(rangeA[0], rangeA[1] + 1):
                        inputsA[gate_from.id - rangeA[0]].append(new_not.id)
                    else:
                        inputsB[gate_from.id - rangeB[0]].append(new_not.id)
                else:
                    gate_to_update.pre_a = None

                    inputs[gate_to_update.id] = gate_to_update
                    if gate_from.id in range(rangeA[0], rangeA[1] + 1):
                        inputsA[gate_from.id - rangeA[0]].append(gate_to_update.id)
                    else:
                        inputsB[gate_from.id - rangeB[0]].append(gate_to_update.id)

            elif gate_to[1] == 1:
                if gate_to_update.pre_b == mark_as_or:
                    new_not = AND((len(gatelist) + 1) * 10, person, None, None, True)
                    new_not.next.append((gate_to_update, Gate.WIRE_B))
                    gatelist.append(new_not)
                    gate_to_update.pre_b = new_not

                    inputs[new_not.id] = new_not
                    if gate_from.id in range(rangeA[0], rangeA[1] + 1):
                        inputsA[gate_from.id - rangeA[0]].append(new_not.id + 1)
                    else:
                        inputsB[gate_from.id - rangeB[0]].append(new_not.id + 1)

                else:
                    gate_to_update.pre_b = None

                    inputs[gate_to_update.id] = gate_to_update
                    if gate_from.id in range(rangeA[0], rangeA[1] + 1):
                        inputsA[gate_from.id - rangeA[0]].append(gate_to_update.id + 1)
                    else:
                        inputsB[gate_from.id - rangeB[0]].append(gate_to_update.id + 1)

    # turn output mapping into list for mapping
    outputs = []
    for i in sorted(output_mapping.keys()):
        out = gatelist[output_mapping[i] - 1]
        # add gate to output list if two predecessors exist and both has valid gate IDs (greater 0)
        if out.pre_a and out.pre_b:
            if out.pre_a.id >= 0 and out.pre_b.id >= 0:
                outputs.append(out)
        # add gate if one predecessor is a valid gate and one is a direct input
        elif out.pre_a and (h.id_in_list(out.id + 1, inputsA) or h.id_in_list(out.id + 1, inputsB)):
            if out.pre_a.id >= 0:
                outputs.append(out)
        elif out.pre_b and (h.id_in_list(out.id, inputsA) or h.id_in_list(out.id, inputsB)):
            if out.pre_b.id >= 0:
                outputs.append(out)
        # add gate if both predecessors are direct inputs
        elif (h.id_in_list(out.id + 1, inputsA) or h.id_in_list(out.id + 1, inputsB)) and (
                h.id_in_list(out.id, inputsA) or h.id_in_list(out.id, inputsB)):
            outputs.append(out)

    # reverse input lists and assign them to the person
    inputsA = [i for i in reversed(inputsA)]
    inputsB = [i for i in reversed(inputsB)]
    person.inputs = inputsA if person.x == Person.A else inputsB
    person.other_inputs = inputsB if person.x == Person.A else inputsA

    num_and = 0
    for gate in gatelist:
        if gate.type == Gate.TYPE_AND:
            num_and += 1

    # clean circuit files
    # if os.path.isdir(conf.default_output):
    #    shutil.rmtree(conf.default_output)

    if test:
        return inputs, outputs, num_and, gatelist
    else:
        return inputs, outputs, num_and


def create_circuit(circuit_name: str, person: Person, sub_folder=False):
    relative_path = "cbmc_parser/gate_files/"
    if sub_folder:
        relative_path = "../" + relative_path

    if circuit_name in os.listdir(relative_path):
        return create_circuit_from_output_data(circuit_name, person)
    elif circuit_name.split(".")[-1] == "c":
        compiler.cbmc_gc_compile(circuit_name)
        return create_circuit_from_output_data("default_output", person)
    else:
        raise CircuitCreationError()
