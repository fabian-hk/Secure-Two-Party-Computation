from multiprocessing import Process, Queue
from typing import List

from tools.person import Person
from MPC import MPC
from protobuf import Output_pb2
from tests.plain_evaluator import *
from fpre.fpre import Fpre
import conf
import cbmc_parser.create_circuit as cc


def user(id: int, create_circuit, input, q: Queue):
    certificate = "certificate-alice" if id == 0 else "certificate-bob"
    partner = "bob.mpc" if id == 0 else "alice.mpc"

    com = Fpre(conf.test_server_ip, conf.test_server_port, certificate, partner)
    mpc = MPC(com)
    mpc.function_independent_preprocessing()

    if type(create_circuit) == str:
        inputs, outputs, num_and = cc.create_circuit(create_circuit, com.person)
    else:
        inputs, outputs, num_and = create_circuit(com.person)
    if type(input[com.person.x][0]) == str:
        com.person.load_input_string(input[com.person.x])
    elif type(input[com.person.x][0]) == int:
        com.person.load_input_integer(input[com.person.x])
    else:
        raise TypeError()
    mpc.load_cirucit(inputs, outputs, num_and)

    mpc.function_dependent_preprocessing()

    mpc.input_processing()

    if com.person.x == Person.B:
        mpc.circuit_evaluation()

    result_proto = mpc.output_determination()
    result = protobuf_to_dict(result_proto)

    if com.person.x == Person.B:
        q.put((result, result_proto))


def evaluate(create_circuit, input):
    q = Queue()
    p_a = Process(target=user, args=(0, create_circuit, input, q))
    p_b = Process(target=user, args=(1, create_circuit, input, q,))
    p_a.start()
    p_b.start()
    p_a.join()
    p_b.join()
    return q.get()


def evaluate_circuit(circuit, in_vals_a, in_vals_b, proto_out=False):
    """
    :param circuit:
    :param in_vals_a:
    :param in_vals_b:
    :return (mpc_result, plain_result)
    """
    # do MPC
    res_dict_mpc, res_proto_mpc = evaluate(circuit, [in_vals_a, in_vals_b])

    # evaluate in plain form to check the output
    person_a = Person(Person.A)
    if type(circuit) == str:
        _, outputs, _ = cc.create_circuit(circuit, person_a)
    else:
        _, outputs, _ = circuit(person_a)
    if type(in_vals_a[0]) == str:
        person_a.load_input_string(in_vals_a)
    elif type(in_vals_a[0]) == int:
        person_a.load_input_integer(in_vals_a)
    else:
        raise TypeError()
    person_b = Person(Person.B)
    if type(circuit) == str:
        _, outputs, _ = cc.create_circuit(circuit, person_b)
    else:
        _, outputs, _ = circuit(person_b)
    if type(in_vals_b[0]) == str:
        person_b.load_input_string(in_vals_b)
    elif type(in_vals_b[0]) == int:
        person_b.load_input_integer(in_vals_b)
    else:
        raise TypeError()
    in_vals = person_a.in_vals
    in_vals.update(person_b.in_vals)
    res_dict_plain = plain_circuit_evaluation(outputs, in_vals)

    if not proto_out:
        return res_dict_mpc, res_dict_plain
    else:
        return res_proto_mpc, res_dict_mpc, res_dict_plain


def protobuf_to_dict(proto: Output_pb2.Outputs):
    result = {}
    for res in proto.outputs:
        result[res.id - 2] = res.output
    return result
