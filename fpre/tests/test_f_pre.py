import unittest
from multiprocessing import Process, Queue
from random import randint

from fpre.fpre import Fpre
import fpre.f_a_and as faand
from fpre.f_ha_and import f_ha_and
import fpre.f_la_and as flaand
from protobuf import FunctionDependentPreprocessing_pb2
from tools.person import Person
import tools.helper as h
import conf


class TestFpre(unittest.TestCase):

    def run_f_a_and(self, id, q, p):
        certificate = "certificate-alice" if id == 0 else "certificate-bob"
        partner = "bob.mpc" if id == 0 else "alice.mpc"

        com = Fpre(conf.test_server_ip, conf.test_server_port, certificate, partner)
        com.init_fpre()

        auth_bits = flaand.get_authbits(com.person, com, 2)
        and_triple = FunctionDependentPreprocessing_pb2.ANDTriple()
        and_triple.id = 0
        auth_bits = iter(auth_bits.bits)
        auth_bit = next(auth_bits)
        and_triple.r1 = auth_bit.r
        and_triple.M1 = auth_bit.M
        and_triple.K1 = auth_bit.K
        auth_bit = next(auth_bits)
        and_triple.r2 = auth_bit.r
        and_triple.M2 = auth_bit.M
        and_triple.K2 = auth_bit.K

        faand.f_a_and(com.person, com, and_triple)
        com.close_session()
        if com.person.x == Person.A:
            q.put((com.person.delta, and_triple))
        else:
            p.put((com.person.delta, and_triple))

    def test_f_a_and(self):
        for i in range(20):
            q = Queue()
            p = Queue()
            pa = Process(target=self.run_f_a_and, args=(0, q, p,))
            pb = Process(target=self.run_f_a_and, args=(1, q, p,))
            pa.start()
            pb.start()
            pa.join()
            pb.join()
            delta_a, and_triple_a = q.get()
            delta_b, and_triple_b = p.get()
            self.assertTrue(h.check_and_triple(and_triple_a, and_triple_b, delta_a, delta_b, True))

    def run_f_la_and(self, id, q, p):
        certificate = "certificate-alice" if id == 0 else "certificate-bob"
        partner = "bob.mpc" if id == 0 else "alice.mpc"

        com = Fpre(conf.test_server_ip, conf.test_server_port, certificate, partner)
        com.init_fpre()
        and_triple = FunctionDependentPreprocessing_pb2.ANDTriple()
        and_triple.id = 0
        flaand.f_la_and(com, com.person, and_triple)
        com.close_session()
        if com.person.x == Person.A:
            q.put((com.person.delta, and_triple))
        else:
            p.put((com.person.delta, and_triple))

    def test_f_la_and(self):
        for i in range(10):
            q = Queue()
            p = Queue()
            pa = Process(target=self.run_f_la_and, args=(0, q, p,))
            pb = Process(target=self.run_f_la_and, args=(1, q, p,))
            pa.start()
            pb.start()
            pa.join()
            pb.join()
            delta_a, and_triple_a = q.get()
            delta_b, and_triple_b = p.get()
            i = 0
            self.assertTrue(h.check_and_triple(and_triple_a, and_triple_b, delta_a, delta_b, True))

    """
    def run_compute_and_triple(self, id, q, p):
        certificate = "certificate-alice" if id == 0 else "certificate-bob"
        partner = "bob.mpc" if id == 0 else "alice.mpc"

        com = Fpre(conf.test_server_ip, conf.test_server_port, certificate, partner)
        com.init_fpre()
        auth_bits = flaand.get_authbits(com.person, com, 2)
        and_triple = FunctionDependentPreprocessing_pb2.ANDTriple()
        and_triple.id = 0
        auth_bits = iter(auth_bits.bits)
        auth_bit = next(auth_bits)
        and_triple.r1 = auth_bit.r
        and_triple.M1 = auth_bit.M
        and_triple.K1 = auth_bit.K
        auth_bit = next(auth_bits)
        and_triple.r2 = auth_bit.r
        and_triple.M2 = auth_bit.M
        and_triple.K2 = auth_bit.K

        and_triples = faand.f_a_and(com.person, com, 1)

        faand.compute_and_triple(and_triple, next(iter(and_triples.triples)), com, com.person)

        com.close_session()
        if com.person.x == Person.A:
            q.put((com.person.delta, and_triple))
        else:
            p.put((com.person.delta, and_triple))

    def test_compute_and_triple(self):
        q = Queue()
        p = Queue()
        pa = Process(target=self.run_compute_and_triple, args=(0, q, p,))
        pb = Process(target=self.run_compute_and_triple, args=(1, q, p,))
        pa.start()
        pb.start()
        pa.join()
        pb.join()
        delta_a, and_triple_a = q.get()
        delta_b, and_triple_b = p.get()
        self.assertTrue(h.check_and_triple(and_triple_a, and_triple_b, delta_a, delta_b, True))
    """

    def run_f_ha_and(self, id, q, p):
        certificate = "certificate-alice" if id == 0 else "certificate-bob"
        partner = "bob.mpc" if id == 0 else "alice.mpc"

        com = Fpre(conf.test_server_ip, conf.test_server_port, certificate, partner)
        com.init_fpre()

        y = randint(0, 1).to_bytes(1, byteorder='big')
        auth_bits = flaand.get_authbits(com.person, com, 1)
        auth_bit = iter(auth_bits.bits).__next__()

        v = f_ha_and(com.person, com, y, auth_bit.r, auth_bit.M, auth_bit.K)

        com.close_session()
        if com.person.x == Person.A:
            p.put((com.person.delta, v, auth_bit, y))
        else:
            q.put((com.person.delta, v, auth_bit, y))

    def test_f_ha_and(self):
        for i in range(10):
            q = Queue()
            p = Queue()
            pa = Process(target=self.run_f_ha_and, args=(0, q, p,))
            pb = Process(target=self.run_f_ha_and, args=(1, q, p,))
            pa.start()
            pb.start()
            pa.join()
            pb.join()
            delta_a, v_a, auth_bit_a, y_a = p.get()
            delta_b, v_b, auth_bit_b, y_b = q.get()
            print("xor", h.xor(v_a, v_b), h.xor(h.AND(auth_bit_a.r, y_b), h.AND(auth_bit_b.r, y_a)))
            self.assertEqual(h.xor(v_a, v_b), h.xor(h.AND(auth_bit_a.r, y_b), h.AND(auth_bit_b.r, y_a)))
