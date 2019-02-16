import csv
import gate as gc


class SimpleGate:
    TYPE_AND = 0
    TYPE_XOR = 1
    TYPE_INV = 2

    def __init__(self, id, pre_a, pre_b, next, gate_type):
        self.id = id
        self.pre_a = pre_a
        self.pre_b = pre_b
        self.next = next
        self.gate_type = gate_type

    def __str__(self):
        return("gate-id: " + str(self.id) + "   input-wire-ids: " + str(self.pre_a) + ", " + str(self.pre_b) + "   "
                "output-wire-id: " + str(self.next) + "   type: " + str(self.gate_type))

def bristol_to_simplegatelist():
    file_add = open('gate_files/add_bristol.txt', 'r', newline='', encoding="utf8")
    file_eucl = open('gate_files/eucl_dist_bristol.txt', 'r', newline='', encoding="utf8")
    reader = csv.reader(file_eucl, delimiter=' ', quoting=csv.QUOTE_NONE)

    num_of_gates = 0
    num_of_wires = 0

    num_of_input_bits_a = 0
    num_of_input_bits_b = 0

    num_of_output_bits = 0

    list_of_gates = []

    gate_iterator = iter(reader)
    row1 = next(gate_iterator)
    num_of_gates = row1[0]
    num_of_wires = row1[1]
    gatetype = ''
    next(gate_iterator)
    next(gate_iterator)

    id = 0

    for gate in gate_iterator:
        num_of_inputs = int(gate[0])
        num_of_outputs = int(gate[1])
        inputs = []
        outputs = []

        for i in range(2, 2 + num_of_inputs):
            inputs.append(int(gate[i]))
        for i in range(2 + num_of_inputs, 2 + num_of_inputs + num_of_outputs):
            outputs.append(int(gate[i]))

        gatetype = gate[2 + num_of_inputs + num_of_outputs]

        if num_of_inputs > 2:
            raise Exception('too many inputs to gate: {}'.format(id))
        if num_of_outputs > 1:
            raise Exception('too many outputs to gate: {}'.format(id))

        if gatetype == 'INV':
            list_of_gates.append(SimpleGate(id, inputs[0], inputs[0], outputs[0], 2))
            id += 1
        elif gatetype == 'AND':
            list_of_gates.append(SimpleGate(id, inputs[0], inputs[1], outputs[0], 0))
            id += 1
            pass
        elif gatetype == 'XOR':
            list_of_gates.append(SimpleGate(id, inputs[0], inputs[1], outputs[0], 1))
            id += 1
        else:
            raise Exception('unknown gate type: {}'.format(gatetype))

    for gate in list_of_gates:
        print(gate)

bristol_to_simplegatelist()