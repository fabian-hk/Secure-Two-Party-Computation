import hashlib
import os
import conf


from tools.person import Person
from fpre.fpre  import Fpre

def f_eq(person: Person, communiator: Fpre, R):
    if person.x == person.A:
        x = R
        r = os.urandom(int(conf.k/8))
        hash_function = hashlib.sha3_256()
        hash_function.update(x + r)
        c = hash_function.digest()
        #connections
        nothing = communiator.exchange_data(c)
        y = communiator.exchange_data()
        nothing = communiator.exchange_data(x)
        nothing = communiator.exchange_data(r)
        if y == x:
            return True
        else:
            return False
    else:
        y = R
        c = communiator.exchange_data()
        nothing = communiator.exchange_data(y)
        x = communiator.exchange_data()
        r = communiator.exchange_data()
        hash_function = hashlib.sha3_256()
        hash_function.update(x + r)
        if hash_function.digest() == c and x == y:
            return True
        else:
            return False