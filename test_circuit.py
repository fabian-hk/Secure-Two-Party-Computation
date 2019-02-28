import parse_native_format

def int_to_bytes(input):
    """
    Only for unsigned integers

    :param input:
    :return:
    """
    return input.to_bytes((input.bit_length() + 7) // 8, 'big')

def int_to_bitstring32(input):

    #TODO negative integers dont work

    bitstring = bin(int(str(input), base=10))[2:]

    if len(bitstring) > 32:
        raise Exception('integer too big')

    bitstring = ((32 - len(bitstring)) * '0') + bitstring
    return bitstring

def test_circuit(output_file, inputA, inputB):
    """
    Test circuit for two 32 bit integers as input

    :param output_file:
    :param inputA: Integer
    :param inputB: Integer
    :return:
    """
    input_gate_list, rangeA, rangeB, nonio_gate_list = parse_native_format.parse_native(output_file)




