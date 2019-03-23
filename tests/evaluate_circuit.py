from tools.person import Person
from MPC import MPC
from multiprocessing import Process, Queue


def user_a(create_circuit, input_a):
    person = Person(Person.A)
    mpc = MPC(person)

    inputs, outputs = create_circuit(person)
    person.load_input(input_a)
    mpc.load_cirucit(inputs, outputs)

    mpc.function_dependent_preprocessing()

    mpc.input_processing()

    mpc.output_determination()


def user_b(create_circuit, input_b, q: Queue):
    person = Person(Person.B)
    mpc = MPC(person)

    inputs, outputs = create_circuit(person)
    person.load_input(input_b)
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
