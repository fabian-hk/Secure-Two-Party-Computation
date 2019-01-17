from person import Person
import helper as h
import hashlib


class Gate:
    def __init__(self, person, pre_a, pre_b, next):
        self.pre_a = pre_a
        self.pre_b = pre_b
        self.next = next
        self.person = person


class AND(Gate):
    def __init__(self, person, pre_a, pre_b, next):
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
        super().__init__(person, pre_a, pre_b, next)
        self.yi = []
        self.Myi = []
        self.Kyi = []
        self.Gi = []
        self.La0 = None
        self.Lb0 = None
        self.La1 = None
        self.Lb1 = None
        self.Ly0 = None

    def compute_preprocessing(self, a, Ma, Ka, b, Mb, Kb, y, My, Ky, o, Mo, Ko, La0=None, Lb0=None, Ly0=None):
        # Protocol part 4 b) c)
        self.yi[0] = h.xor(o, y)
        self.Myi[0] = h.xor(Mo, My)
        self.Kyi[0] = h.xor(Ko, Ky)

        self.yi[1] = h.xor(o, y, a)
        self.Myi[1] = h.xor(Mo, My, Ma)
        self.Kyi[1] = h.xor(Ko, Ky, Ka)

        self.yi[2] = h.xor(o, y, b)
        self.Myi[2] = h.xor(Mo, My, Mb)
        self.Kyi[2] = h.xor(Ko, Ky, Kb)

        if self.person.x == Person.B:
            self.yi[3] = h.xor(o, y, a, b'\x01')
        else:
            self.yi[3] = h.xor(o, y, a)
        self.Myi[3] = h.xor(Mo, My, Ma, Mb)
        if self.person.x == Person.A:
            self.Kyi[3] = h.xor(Ko, Ky, Ka, Kb, self.person.delta)
        else:
            self.Kyi[3] = h.xor(Ko, Ky, Ka, Kb)

        # Protocol part 4 d)
        if self.person.x == Person.A:
            self.La0 = La0
            self.Lb0 = Lb0
            self.Ly0 = Ly0
            self.La1 = h.xor(self.La0, self.person.delta)
            self.Lb1 = h.xor(self.Lb0, self.person.delta)

            hash_function = hashlib.sha3_256()
            hash_function.update(self.La0+self.Lb0+y+b'\x01')
            tmp1 = hash_function.digest()
            tmp2 = self.yi[0]+self.Myi[0]+h.xor(self.Ly0, self.Kyi[0], self.yi[0]+self.person.delta)
            self.Gi[0] = h.xor(tmp1, tmp2)


class XOR(Gate):
    def __init__(self, person, pre_a, pre_b, next):
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
        super().__init__(person, pre_a, pre_b, next)
        self.y = None
        self.My = None
        self.Ky = None

    def compute_preprocessing(self, a, Ma, Ka, b, Mb, Kb):
        # Protocol part 3
        self.y = h.xor(a, b)
        self.My = h.xor(Ma, Mb)
        self.Ky = h.xor(Ka, Kb)
