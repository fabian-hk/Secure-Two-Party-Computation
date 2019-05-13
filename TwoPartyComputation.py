import argparse

from tools.person import Person
import tools.helper as h
from MPC import MPC
from tests.test_circuit_creater import *
from fpre.fpre import Fpre
import cbmc_parser.create_circuit as cc

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script for maliciously secure Two-Party Computation. '
                                                 'You should start the script from the directory of this repository.',
                                     epilog='Example usage:\n\tpython3 TwoPartyComputation.py add 45 '
                                            '-cn bob.mpc -s 10.10.1.42 -p 4444\n\t'
                                            'python3 TwoPartyComputation.py cbmc_parser/ansi_c_code/addition.c 52 '
                                            '-cn bob.mpc -s 10.10.1.42 -p 4444',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('circuit', type=str,
                        help='Either one of the example circuits or a path to an parsable c-code file (ending .c). '
                             'Path must be relativ to the location of this file.')
    parser.add_argument('input', type=int, nargs='+', help='Own input to the circuit as an Integer.')
    parser.add_argument('-cn', type=str, default=None,
                        help='Common name of the partner you want to talk to.')
    parser.add_argument('-c', '--certificate', type=str, default=None,
                        help='Own certificate to authenticate your self to the other party '
                             '(should be specified in the conf.py file).')
    parser.add_argument('-n', '--noencryption', default=False, action='store_true',
                        help="Specify this option if you don't care about security "
                             "and want to use unencrypted communication")
    parser.add_argument('-s', '--server', type=str, default='127.0.0.1',
                        help='IP address for the server which provides Fpre and the '
                             'communication between the clients.')
    parser.add_argument('-p', '--port', type=int, default=8448,
                        help='The port of the server specified by -s (default 8448).')
    args = parser.parse_args()

    # Initialize connection and determine who is A and who is B
    com = Fpre(args.server, args.port, args.certificate, args.cn, args.noencryption)

    # Initialize MCP class which will do the garbling and evaluation
    mpc = MPC(com)

    # First do the function independent preprocessing to generate authenticated bits
    mpc.function_independent_preprocessing()

    # Parse the circuit and load the inputs for the person
    inputs, outputs, num_and, gatelist = cc.create_circuit(args.circuit, com.person, True)
    try:
        com.person.load_input_integer(args.input)
    except IndexError:
        com.close_session()
        raise
    mpc.load_cirucit(inputs, outputs, num_and, gatelist)

    # Do the function dependent preprocessing which garbles the circuit
    mpc.function_dependent_preprocessing()

    # Create masked input bits
    mpc.input_processing()

    # Person B evaluates the circuit
    if com.person.x == Person.B:
        mpc.circuit_evaluation()

    # Determine the real output values
    result = mpc.output_determination()

    # Print the output as binary and decimal number to the console
    h.print_output(result)
