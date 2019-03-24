from multiprocessing import Process, Queue

from tools.person import Person
from MPC import MPC
from tests.plain_evaluator import *


def user_a(create_circuit, input_a):
    person = Person(Person.A)
    mpc = MPC(person)

    inputs, outputs = create_circuit(person)
    person.load_input_string(input_a)
    mpc.load_cirucit(inputs, outputs)

    mpc.function_dependent_preprocessing()

    mpc.input_processing()

    mpc.output_determination()


def user_b(create_circuit, input_b, q: Queue):
    person = Person(Person.B)
    mpc = MPC(person)

    inputs, outputs = create_circuit(person)
    person.load_input_string(input_b)
    mpc.load_cirucit(inputs, outputs)

    mpc.function_dependent_preprocessing()

    mpc.input_processing()

    mpc.circuit_evaluation()

    result = mpc.output_determination()

    q.put(result)


def evaluate(create_circuit, input_a, input_b):
    q = Queue()
    p_a = Process(target=user_a, args=(create_circuit, input_a))
    p_b = Process(target=user_b, args=(create_circuit, input_b, q,))
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
    res_dict_mpc = evaluate(circuit, in_vals_a, in_vals_b)

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
