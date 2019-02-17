from tools.person import Person
from tools import helper as h
import hashlib
import abc


class Gate:
    TYPE_AND = 0
    TYPE_XOR = 1

    def __init__(self, id, person, pre_a, pre_b, next=None):
        """
        :param id: unique id of the gate (see README for more information)
        :param person:
        :param pre_a:
        :param pre_b:
        :param next:
        """
        self.id = id
        self.pre_a = pre_a  # type: Gate
        if self.pre_a:
            self.pre_a.next = self
        self.pre_b = pre_b  # type: Gate
        if self.pre_b:
            self.pre_b.next = self
        self.next = next
        self.person = person
        self.type = None

    @abc.abstractmethod
    def function_independent_preprocessing(self):
        """
        Method to save the variables in the function independing preprocessing
        :return:
        """
        return

    @abc.abstractmethod
    def function_dependent_preprocessing(self):
        """
        Method to compute the function depending preprocessing of the gate
        :return:
        """
        return


class AND(Gate):
    def __init__(self, id, person, pre_a, pre_b, next=None):
        """
        :param person:
        :type person Person
        :param pre_a:
        :type pre_a Gate
        :param pre_b:
        :type pre_b Gate
        :param next:
        :type next Gate
        """
        super().__init__(id, person, pre_a, pre_b, next)
        self.type = Gate.TYPE_AND
        self.yi = []
        self.Myi = []
        self.Kyi = []
        self.Gi = []
        self.La0 = None
        self.Lb0 = None
        self.La1 = None
        self.Lb1 = None
        self.Ly0 = None

        self.a = None
        self.Ma = None
        self.Ka = None
        self.b = None
        self.Mb = None
        self.Kb = None
        self.y = None
        self.My = None
        self.Ky = None
        self.o = None
        self.Mo = None
        self.Ko = None

    def compute_G(self, i, La, Lb):
        """
        Computes one row of the garbled table
        :param i:
        :param La:
        :param Lb:
        :return:
        """
        hash_function = hashlib.sha3_256()
        # the wire ID is encoded as a 4 byte integer for more information read the README file
        hash_function.update(La + Lb + (self.id+2).to_bytes(4, 'big') + i.to_bytes(1, 'big'))
        tmp1 = hash_function.digest()
        if self.yi[i] == 1:
            tmp2 = self.yi[i] + self.Myi[i] + h.xor(self.Ly0, self.Kyi[i], self.yi[i] + self.person.delta)
        else:
            tmp2 = self.yi[i] + self.Myi[i] + h.xor(self.Ly0, self.Kyi[i])
        return h.xor(tmp1, tmp2)

    def function_dependent_preprocessing(self, ser_gate):
        ser_gate.id = self.id
        # Protocol part 4 b) c)
        self.yi[0] = h.xor(self.o, self.y)
        self.Myi[0] = h.xor(self.Mo, self.My)
        self.Kyi[0] = h.xor(self.Ko, self.Ky)

        self.yi[1] = h.xor(self.o, self.y, self.a)
        self.Myi[1] = h.xor(self.Mo, self.My, self.Ma)
        self.Kyi[1] = h.xor(self.Ko, self.Ky, self.Ka)

        self.yi[2] = h.xor(self.o, self.y, self.b)
        self.Myi[2] = h.xor(self.Mo, self.My, self.Mb)
        self.Kyi[2] = h.xor(self.Ko, self.Ky, self.Kb)

        if self.person.x == Person.B:
            self.yi[3] = h.xor(self.o, self.y, self.a, b'\x01')
        else:
            self.yi[3] = h.xor(self.o, self.y, self.a)
        self.Myi[3] = h.xor(self.Mo, self.My, self.Ma, self.Mb)
        if self.person.x == Person.A:
            self.Kyi[3] = h.xor(self.Ko, self.Ky, self.Ka, self.Kb, self.person.delta)
        else:
            self.Kyi[3] = h.xor(self.Ko, self.Ky, self.Ka, self.Kb)

        # Protocol part 4 d)
        if self.person.x == Person.A:
            self.La1 = h.xor(self.La0, self.person.delta)
            self.Lb1 = h.xor(self.Lb0, self.person.delta)

            self.Gi[0] = self.compute_G(0, self.La0, self.Lb0)
            self.Gi[1] = self.compute_G(1, self.La0, self.Lb1)
            self.Gi[2] = self.compute_G(2, self.La1, self.Lb0)
            self.Gi[3] = self.compute_G(3, self.La1, self.Lb1)
            ser_gate.G0 = self.Gi[0]
            ser_gate.G1 = self.Gi[1]
            ser_gate.G2 = self.Gi[2]
            ser_gate.G3 = self.Gi[3]


class XOR(Gate):
    def __init__(self, id, person, pre_a, pre_b, next=None):
        """
        :param person:
        :type person Person
        :param pre_a:
        :type pre_a Gate
        :param pre_b:
        :type pre_b Gate
        :param next:
        :type next Gate
        """
        super().__init__(id, person, pre_a, pre_b, next)
        self.type = Gate.TYPE_XOR
        self.a = None
        self.Ma = None
        self.Ka = None
        self.b = None
        self.Mb = None
        self.Kb = None
        self.y = None
        self.My = None
        self.Ky = None

    def function_dependent_preprocessing(self):
        # Protocol part 3
        self.y = h.xor(self.a, self.b)
        self.My = h.xor(self.Ma, self.Mb)
        self.Ky = h.xor(self.Ka, self.Kb)
