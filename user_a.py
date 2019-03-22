from tools.person import Person
from MPC import MPC
from tests.circuit_creater import *

if __name__ == "__main__":
    person = Person(Person.A)
    mpc = MPC(person)

    inputs, outputs = create_example_circuit_1(person)
    mpc.load_cirucit(inputs, outputs)

    mpc.function_dependent_preprocessing()

    in_vals = {10: 1, 20: 0}
    other_in = [11, 21]
    mpc.input_processing(in_vals, other_in)

    mpc.output_determination()
