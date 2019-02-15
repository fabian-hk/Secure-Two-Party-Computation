from typing import Dict
from protobuf import FunctionIndependentPreprocessing_pb2, FunctionDependentPreprocessing_pb2
from tools import person, fpre
from gate import *

# holds all gates like {int_id : gate}
circuit: Dict[int, Gate] = {}

# user how currently executes the script
person = person.Person(person.Person.A)


def create_example_circuit():
    and0 = AND(1, person, None, None)
    circuit[1] = and0
    and1 = AND(2, person, None, None)
    circuit[2] = and1
    xor3 = XOR(3, person, and0, and1)
    circuit[3] = xor3
    print("Dictionary with all gates:")
    print(circuit)


def function_independent_preprocessing():
    ser_gates = FunctionIndependentPreprocessing_pb2.GatesPreprocessing()
    for id in circuit.keys():
        ser_gate = ser_gates.gates.add()
        ser_gate.id = id
        g = circuit[id]
        # TODO create all variables for the preprocessing
        if g.type == Gate.TYPE_XOR:
            m0, m1 = fpre.create_gate_vars()
            ser_gate.M0 = m0
            ser_gate.M1 = m1
        elif g.type == Gate.TYPE_AND:
            m0, m1 = fpre.create_gate_vars()
            ser_gate.M0 = m0
            ser_gate.M1 = m1

    # Serialize the tags to send over to the other user
    print("Serialized data to send over to the other user:")
    ser_gates_bytes = ser_gates.SerializeToString()
    print(ser_gates_bytes)
    for g in ser_gates.gates:
        print("Gate ID: " + str(g.id))
        print("M0: " + str(g.M0))
        print("M1: " + str(g.M1))


def function_dependent_preprocessing():
    ser_gates = FunctionDependentPreprocessing_pb2.GatesPreprocessing()
    for id in circuit.keys():
        ser_gate = ser_gates.gates.add()
        g = circuit[id]
        if g.type == Gate.TYPE_XOR:
            m0, m1 = fpre.create_gate_vars()
            ser_gate.M0 = m0
            ser_gate.M1 = m1
        elif g.type == Gate.TYPE_AND:
            g.function_dependent_preprocessing(ser_gates.gates.add())


if __name__ == "__main__":
    create_example_circuit()
    function_independent_preprocessing()
