from tools.person import Person
from MPC import MPC
from tests.circuit_creater import *
from fpre.fpre import Fpre

if __name__ == "__main__":
    com = Fpre()
    mpc = MPC(com)

    inputs, outputs = create_example_circuit_3(com.person)
    com.person.load_input_string("10")
    mpc.load_cirucit(inputs, outputs)

    mpc.function_dependent_preprocessing()

    mpc.input_processing()

    mpc.output_determination()
