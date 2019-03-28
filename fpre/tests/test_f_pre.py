import unittest
from multiprocessing import Process, Queue

from fpre.fpre import Fpre
from fpre.f_a_and import f_a_and
from tools.person import Person
import tools.helper as h


class TestFpre(unittest.TestCase):

    def run_f_a_and(self, q, p):
        com = Fpre('localhost', 8448)
        com.init_fpre()
        and_triples = f_a_and(com.person, com)
        com.close_session()
        if com.person.x == Person.A:
            q.put((com.person.delta, and_triples))
        else:
            p.put((com.person.delta, and_triples))

    def test_f_a_and(self):
        q = Queue()
        p = Queue()
        pa = Process(target=self.run_f_a_and, args=(q, p,))
        pb = Process(target=self.run_f_a_and, args=(q, p,))
        pa.start()
        pb.start()
        pa.join()
        pb.join()
        delta_a, and_triples_a = q.get()
        delta_b, and_triples_b = p.get()
        i = 0
        for and_triple_a, and_triple_b in zip(and_triples_a.triples, and_triples_b.triples):
            self.assertTrue(h.check_and_triple(and_triple_a, and_triple_b, delta_a, delta_b, True))
            i += 1
        print("Computed "+str(i)+" and triples")
