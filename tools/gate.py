import hashlib
import abc

from tools.person import Person
from tools import helper as h
from fpre.fpre import Fpre
import conf
from exceptions.CheaterException import CheaterRecognized


class Gate:
    TYPE_AND = 0
    TYPE_XOR = 1

    WIRE_A = 0
    WIRE_B = 1
    WIRE_Y = 2

    def __init__(self, id: int, person: Person, pre_a, pre_b):
        """
        :param id: unique id of the gate (see README for more information)
        :type id int
        :param person:
        :param pre_a:
        :type pre_a Gate
        :param pre_b:
        :type pre_b Gate
        :param next:
        """
        self.id = id
        self.next = []
        self.pre_a = pre_a
        if self.pre_a:
            self.pre_a.next.append((self, Gate.WIRE_A))
        self.pre_b = pre_b
        if self.pre_b:
            self.pre_b.next.append((self, Gate.WIRE_B))

        self.person = person
        self.type = None
        self.prepro = False
        self.evaluated = False

        self.La0 = None
        self.Lb0 = None
        self.Ly0 = None
        self.La1 = None
        self.Lb1 = None
        self.Ly1 = None
        self.label_a = None  # label for B during evaluation
        self.label_b = None  # label for B during evaluation
        self.label_y = None  # label for B during evaluation

        self.masked_bit_a = None  # masked bit for B during evaluation
        self.masked_bit_b = None  # masked bit for B during evaluation
        self.masked_bit_y = None  # masked bit for B during evaluation
        self.a = None
        self.Ma = None
        self.Ka = None
        self.b = None
        self.Mb = None
        self.Kb = None
        self.y = None
        self.My = None
        self.Ky = None

    def __str__(self):
        return "\nGate ID: " + str(self.id) + " Type: " + str(self.type) + "\na: " + str(
            self.a) + " b: " + str(self.b) + " y: " + str(self.y) + "\nmasked_a: " + str(
            self.masked_bit_a) + " masked_b: " + str(self.masked_bit_b) + " masked_y: " + str(
            self.masked_bit_y) + "\nLa0: " + str(self.La0) + "\nLa1: " + str(self.La1) + "\nLb0: " + str(
            self.Lb0) + "\nLb1" + str(self.Lb1)

    def initialize_vars(self, auth_bit_A=None, auth_bit_B=None, and_triple=None):
        if auth_bit_A:
            self.a = auth_bit_A.r
            self.Ma = auth_bit_A.M
            self.Ka = auth_bit_A.K
            if and_triple:
                self.get_auth_bit(and_triple, self.WIRE_A)
        if auth_bit_B:
            self.b = auth_bit_B.r
            self.Mb = auth_bit_B.M
            self.Kb = auth_bit_B.K
            if and_triple:
                self.get_auth_bit(and_triple, self.WIRE_B)

    def get_auth_bit(self, and_triple, wire):
        """
        Packs the authenticated bit into an and triple protobuf message.
        :param and_triple: protobuf message
        :param wire: wire A or B
        """
        if wire == self.WIRE_A:
            and_triple.r1 = bytes(self.a)
            and_triple.M1 = bytes(self.Ma)
            and_triple.K1 = bytes(self.Ka)
        if wire == self.WIRE_B:
            and_triple.r2 = bytes(self.b)
            and_triple.M2 = bytes(self.Mb)
            and_triple.K2 = bytes(self.Kb)

    def get_y_auth_bit(self, auth_bit):
        auth_bit.id = self.id
        auth_bit.r = bytes(self.y)
        auth_bit.M = bytes(self.My)

    @abc.abstractmethod
    def function_dependent_preprocessing(self):
        """
        Method to compute the function depending preprocessing of the gate
        :return:
        """
        return

    @abc.abstractmethod
    def circuit_evaluation(self, garbled_gate=None):
        """
        Method to evaluate a single gate
        """
        return


class AND(Gate):
    def __init__(self, id, person, pre_a, pre_b, is_nand=False):
        """
        :param person:
        :type person Person
        :param pre_a:
        :type pre_a Gate
        :param pre_b:
        :type pre_b Gate
        """
        super().__init__(id, person, pre_a, pre_b)
        self.type = Gate.TYPE_AND
        self.is_nand = is_nand
        self.yi = []
        self.Myi = []
        self.Kyi = []
        self.Gi = []

        self.o = None
        self.Mo = None
        self.Ko = None

    def __str__(self):
        return super().__str__() + " o: " + str(self.o) + "\n"

    def initialize_auth_bit_o(self, and_triple):
        self.o = and_triple.r3
        self.Mo = and_triple.M3
        self.Ko = and_triple.K3

    def initialize_auth_bit_y(self, auth_bit):
        self.y = auth_bit.r
        self.My = auth_bit.M
        self.Ky = auth_bit.K

    def compute_G(self, i, La, Lb):
        """
        Computes one row of the garbled table
        :param i:
        :param La:
        :param Lb:
        :return:
        """
        hash_function = hashlib.sha3_512()
        # the wire ID is encoded as a 4 byte integer for more information read the README file
        hash_function.update(La + Lb + (self.id + 2).to_bytes(4, 'big') + i.to_bytes(1, 'big'))
        key = hash_function.digest()
        if self.yi[i] == b'\x01':
            plain = self.yi[i] + self.Myi[i] + h.xor(self.Ly0, self.Kyi[i], self.person.delta)
        else:
            plain = self.yi[i] + self.Myi[i] + h.xor(self.Ly0, self.Kyi[i])
        return h.xor(key, plain)

    def function_dependent_preprocessing(self, ser_gate=None):
        # Protocol part 4 b) c)
        self.yi.append(h.xor(self.o, self.y))
        self.Myi.append(h.xor(self.Mo, self.My))
        self.Kyi.append(h.xor(self.Ko, self.Ky))

        self.yi.append(h.xor(self.o, self.y, self.a))
        self.Myi.append(h.xor(self.Mo, self.My, self.Ma))
        self.Kyi.append(h.xor(self.Ko, self.Ky, self.Ka))

        self.yi.append(h.xor(self.o, self.y, self.b))
        self.Myi.append(h.xor(self.Mo, self.My, self.Mb))
        self.Kyi.append(h.xor(self.Ko, self.Ky, self.Kb))

        if self.person.x == Person.B:
            self.yi.append(h.xor(self.o, self.y, self.a, self.b, b'\x01'))
        else:
            self.yi.append(h.xor(self.o, self.y, self.a, self.b))
        self.Myi.append(h.xor(self.Mo, self.My, self.Ma, self.Mb))
        if self.person.x == Person.A:
            self.Kyi.append(h.xor(self.Ko, self.Ky, self.Ka, self.Kb, self.person.delta))
        else:
            self.Kyi.append(h.xor(self.Ko, self.Ky, self.Ka, self.Kb))

        # Protocol part 4 d)
        if self.person.x == Person.A:
            self.La1 = h.xor(self.La0, self.person.delta)
            self.Lb1 = h.xor(self.Lb0, self.person.delta)

            self.Gi.append(self.compute_G(0, self.La0, self.Lb0))
            self.Gi.append(self.compute_G(1, self.La0, self.Lb1))
            self.Gi.append(self.compute_G(2, self.La1, self.Lb0))
            self.Gi.append(self.compute_G(3, self.La1, self.Lb1))

            # prepare the garbled gate to send over the wire as a byte object
            ser_gate.id = self.id
            ser_gate.G0 = bytes(self.Gi[0])
            ser_gate.G1 = bytes(self.Gi[1])
            ser_gate.G2 = bytes(self.Gi[2])
            ser_gate.G3 = bytes(self.Gi[3])

    def circuit_evaluation(self, garbled_gate=None):
        i = 2 * int.from_bytes(self.masked_bit_a, byteorder='big') + int.from_bytes(self.masked_bit_b, byteorder='big')
        hash_function = hashlib.sha3_512()
        # the wire ID is encoded as a 4 byte integer for more information read the README file
        hash_function.update(self.label_a + self.label_b + (self.id + 2).to_bytes(4, 'big') + i.to_bytes(1, 'big'))
        key = hash_function.digest()
        if i == 0:
            plain = h.xor(garbled_gate.G0, key)
            plain1 = h.xor(garbled_gate.G1, key)
            plain2 = h.xor(garbled_gate.G2, key)
            plain3 = h.xor(garbled_gate.G3, key)
        elif i == 1:
            plain = h.xor(garbled_gate.G1, key)
            plain0 = h.xor(garbled_gate.G0, key)
            plain2 = h.xor(garbled_gate.G2, key)
            plain3 = h.xor(garbled_gate.G3, key)
        elif i == 2:
            plain = h.xor(garbled_gate.G2, key)
            plain0 = h.xor(garbled_gate.G0, key)
            plain1 = h.xor(garbled_gate.G1, key)
            plain3 = h.xor(garbled_gate.G3, key)
        elif i == 3:
            plain = h.xor(garbled_gate.G3, key)
            plain0 = h.xor(garbled_gate.G0, key)
            plain1 = h.xor(garbled_gate.G1, key)
            plain2 = h.xor(garbled_gate.G2, key)

        label = plain[-int(conf.k / 8):]
        Mr = plain[-2 * int(conf.k / 8):-int(conf.k / 8)]
        r = plain[-2 * int(conf.k / 8) - 1:-2 * int(conf.k / 8)]

        # check authenticated bit
        if r == b'\x01':
            if Mr != h.xor(self.Kyi[i], self.person.delta):
                raise CheaterRecognized()
        else:
            if Mr != self.Kyi[i]:
                raise CheaterRecognized()

        self.masked_bit_y = h.xor(self.yi[i], r) if not self.is_nand else h.xor(self.yi[i], r, b'\x01')
        self.label_y = h.xor(label, self.Myi[i])


class XOR(Gate):
    def __init__(self, id, person, pre_a, pre_b):
        """
        :param person:
        :type person Person
        :param pre_a:
        :type pre_a Gate
        :param pre_b:
        :type pre_b Gate
        """
        super().__init__(id, person, pre_a, pre_b)
        self.type = Gate.TYPE_XOR

    def function_dependent_preprocessing(self):
        # Protocol part 3
        if self.person.x == Person.A:
            self.Ly0 = h.xor(self.La0, self.Lb0)

        self.y = h.xor(self.a, self.b)
        self.My = h.xor(self.Ma, self.Mb)
        self.Ky = h.xor(self.Ka, self.Kb)

    def circuit_evaluation(self, garbled_gate=None):
        self.masked_bit_y = h.xor(self.masked_bit_a, self.masked_bit_b)
        self.label_y = h.xor(self.label_a, self.label_b)
