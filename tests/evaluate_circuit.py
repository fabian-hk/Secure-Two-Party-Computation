from multiprocessing import Process, Queue

from tools.person import Person
from MPC import MPC
from tests.plain_evaluator import *
from fpre.fpre import Fpre
import conf


def user(create_circuit, input, q: Queue):
    com = Fpre(conf.test_server_ip, conf.test_server_port)
    mpc = MPC(com)

    inputs, outputs = create_circuit(com.person)
    com.person.load_input_string(input[com.person.x])
    mpc.load_cirucit(inputs, outputs)

    mpc.function_dependent_preprocessing()

    mpc.input_processing()

    if com.person.x == Person.B:
        mpc.circuit_evaluation()

    result = mpc.output_determination()

    if com.person.x == Person.B:
        q.put(result)


def evaluate(create_circuit, input):
    q = Queue()
    p_a = Process(target=user, args=(create_circuit, input, q))
    p_b = Process(target=user, args=(create_circuit, input, q,))
    p_a.start()
    p_b.start()
    p_a.join()
    p_b.join()
    return q.get()


def evaluate_circuit(circuit, in_vals_a, in_vals_b):
    """
    :param circuit:
    :param in_vals_a:
    :param in_vals_b:
    :return (mpc_result, plain_result)
    """
    # do MPC
    res_dict_mpc = evaluate(circuit, [in_vals_a, in_vals_b])

    # evaluate in plain form to check the output
    person_a = Person(Person.A)
    _, outputs = circuit(person_a)
    person_a.load_input_string(in_vals_a)
    person_b = Person(Person.B)
    _, outputs = circuit(person_b)
    person_b.load_input_string(in_vals_b)
    in_vals = person_a.in_vals
    in_vals.update(person_b.in_vals)
    res_dict_plain = plain_circuit_evaluation(outputs, in_vals)

    return res_dict_mpc, res_dict_plain
