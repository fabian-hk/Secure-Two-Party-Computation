from tools.person import Person
from MPC import MPC
from tests.circuit_creater import *

if __name__ == "__main__":
    person = Person(Person.B)
    mpc = MPC(person)

    inputs, outputs = create_example_circuit_3(person)
    person.load_input_string("01")
    mpc.load_cirucit(inputs, outputs)

    mpc.function_dependent_preprocessing()

    mpc.input_processing()

    mpc.circuit_evaluation()

    mpc.output_determination()
