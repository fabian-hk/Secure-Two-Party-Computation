class GateHelper:

    def __init__(self, id, type, num_of_inputs, output_to, is_circuit_output, output_number_list):
        # self.id, together with the self.type forms a unique identifier (since Input Gates have ids 1 to size-of-input)
        self.id = id
        # types used are strings: INPUT, AND, OR, XOR, NOT, NAND
        self.type = type

        # number of inputs that a gate has - all except NOT have 2
        self.num_of_inputs = num_of_inputs

        # ids of gates which this gate outputs to as a tuple with the input on the gate
        self.output_to = output_to

        # boolean flag set if gate output is circuit output
        self.is_circuit_output = is_circuit_output

        # output of this gate used for evaluation of circuit
        self.output_value = None

        # the id of the output bits whose value is the same as this gates output value
        # should be empty if is_circuit_output = False
        self.output_number_list = output_number_list
