from tools.person import Person
from MPC import MPC

if __name__ == "__main__":
    person = Person(Person.B)
    mpc = MPC(person)
    in_vals = {11: 1, 21: 1}
    other_in = [10, 20]
    mpc.input_processing(in_vals, other_in)

    mpc.circuit_evaluation()
