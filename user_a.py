from tools.person import Person
from MPC import MPC
from tests.circuit_creater import *

if __name__ == "__main__":
    person = Person(Person.A)
    mpc = MPC(person)

    inputs, outputs = create_example_circuit_1(person)
    person.load_input("00")
    mpc.load_cirucit(inputs, outputs)

    mpc.function_dependent_preprocessing()

    mpc.input_processing()

    mpc.output_determination()
