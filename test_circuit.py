import parse_native_format


def int_to_bytes(input):
    """
    Only for unsigned integers

    :param input:
    :return:
    """
    return input.to_bytes((input.bit_length() + 7) // 8, 'big')


def int_to_bitstring32(input):
    # TODO negative integers dont work and only poistive integers work

    if int(input) != input:
        raise Exception('input was not an integer')

    if input < 0:
        raise Exception('integer negative')

    bitstring = bin(int(str(input), base=10))[2:]

    if len(bitstring) > 32:
        raise Exception('integer too big')

    bitstring = ((32 - len(bitstring)) * '0') + bitstring
    return bitstring


def assign_input_gates(input_gate_list, input_bitstring, range_of_inputgateid):
    """

    :param input_gate_list: list of objects of type parse_parse_native_format.gate_helper
    :param input_bitstring:
    :param range: tuple of two Integers
    :return:
    """

    count = 1
    for i in range(range_of_inputgateid[0], range_of_inputgateid[1] + 1):
        input_gate_list[i - 1].output_value = bool(int(input_bitstring[-count]))
        count += 1


def test_circuit(output_file, inputA, inputB):
    """
    Test circuit for two 32 bit integers as input

    :param output_file: Folder path string
    :param inputA: Integer
    :param inputB: Integer
    :return:
    """
    input_gate_list, rangeA, rangeB, nonio_gate_list = parse_native_format.parse_native(output_file)

    inputA_bitstring = int_to_bitstring32(inputA)
    inputB_bitstring = int_to_bitstring32(inputB)

    print(rangeA)
    print(rangeB)
    print(inputA_bitstring)
    print(inputB_bitstring)

    assign_input_gates(input_gate_list, inputA_bitstring, rangeA)
    assign_input_gates(input_gate_list, inputB_bitstring, rangeB)

    for a in input_gate_list:
        print(a.output_value)



test_circuit('add_output', 1, 3)
