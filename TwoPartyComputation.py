import argparse

from tools.person import Person
import tools.helper as h
from MPC import MPC
from tests.test_circuit_creater import *
from fpre.fpre import Fpre
import cbmc_parser.create_circuit as cc

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script for maliciously secure Two-Party Computation.',
                                     epilog='Example usage:\n\tpython3 TwoPartyComputation.py and_op 45 '
                                            '-cn bob.mpc -s 10.10.1.42 -p 4444',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('circuit', type=str,
                        help='Either one of the example circuits or a path to an parsable c-code file.')
    parser.add_argument('input', type=int, help='Own input to the circuit as an Integer.')
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

    com = Fpre(args.server, args.port, args.certificate, args.cn, args.noencryption)
    mpc = MPC(com)
    mpc.function_independent_preprocessing()

    if args.circuit == "and_op":
        inputs, outputs, num_and = and_operation(com.person)
    elif args.circuit == "add":
        inputs, outputs, num_and = cc.create_circuit_from_output_data("add_output", com.person)
    com.person.load_input_integer(args.input)
    mpc.load_cirucit(inputs, outputs, num_and)

    mpc.function_dependent_preprocessing()

    mpc.input_processing()

    if com.person.x == Person.B:
        mpc.circuit_evaluation()

    result = mpc.output_determination()

    h.print_output(result)
