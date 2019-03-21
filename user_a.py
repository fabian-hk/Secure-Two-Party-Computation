from tools.person import Person
from MPC import MPC

if __name__ == "__main__":
    person = Person(Person.A)
    mpc = MPC(person)
    in_vals = {10: 0, 20: 1}
    mpc.input_preprocessing(in_vals)
