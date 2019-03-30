import argparse

from tools.person import Person
from MPC import MPC
from tests.test_circuit_creater import *
from fpre.fpre import Fpre

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script for maliciously secure Two-Party Computation.',
                                     epilog='Example usage:\n\tpython3 TwoPartyComputation.py and_op 45 -s 10.10.1.42 -p 4444',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('circuit', type=str,
                        help='Either one of the example circuits or a path to an parsable c-code file.')
    parser.add_argument('input', type=int, help='Own input to the circuit as an Integer.')
    parser.add_argument('-s', '--server', type=str, default='127.0.0.1',
                        help='IP address for the server which provides Fpre and the communication bewtween the clients.')
    parser.add_argument('-p', '--port', type=int, default=8448,
                        help='The port of the server specified by -s (default 8448).')
    args = parser.parse_args()

    com = Fpre(args.server, args.port)
    mpc = MPC(com)

    if args.circuit == "and_op":
        inputs, outputs = and_operation(com.person)
        com.person.load_input_integer(args.input)
    mpc.load_cirucit(inputs, outputs)

    mpc.function_dependent_preprocessing()

    mpc.input_processing()

    if com.person.x == Person.B:
        mpc.circuit_evaluation()

    mpc.output_determination()
