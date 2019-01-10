from person import Person


class Gate:
    def __init__(self, person, pre_a, pre_b, next, a, Ma, Ka, b, Mb, Kb):
        self.a = a
        self.Ma = Ma
        self.Ka = Ka
        self.b = b
        self.Mb = Mb
        self.Kb = Kb

        self.pre_a = pre_a
        self.pre_b = pre_b
        self.next = next


class AND(Gate):
    def __init__(self, person, pre_a, pre_b, next, a, Ma, Ka, b, Mb, Kb, y, My, Ky, o, Mo, Ko):
        """
        :param person:
        :type person Person
        :param pre_a:
        :param pre_b:
        :param next:
        :param a:
        :param Ma:
        :param Ka:
        :param b:
        :param Mb:
        :param Kb:
        :param y:
        :param My:
        :param Ky:
        :param o:
        :param Mo:
        :param Ko:
        """
        super().__init__(x, pre_a, pre_b, next, a, Ma, Ka, b, Mb, Kb)

        # Protocol part 4 b) c)
        self.y[0] = o ^ y
        self.My[0] = Mo ^ My
        self.Ky[0] = Ko ^ Ky

        self.y[1] = o ^ y ^ a
        self.My[1] = Mo ^ My ^ Ma
        self.Ky[1] = Ko ^ Ky ^ Ka

        self.y[2] = o ^ y ^ b
        self.My[2] = Mo ^ My ^ Mb
        self.Ky[2] = Ko ^ Ky ^ Kb

        if person.x == Person.B:
            self.y[3] = o ^ y ^ a ^ 1
        else:
            self.y[3] = o ^ y ^ a
        self.My[3] = Mo ^ My ^ Ma ^ Mb
        if person.x == Person.A:
            self.Ky[3] = Ko ^ Ky ^ Ka ^ Kb ^ person.delta
        else:
            self.Ky[3] = Ko ^ Ky ^ Ka ^ Kb

        # Protocol part 4 d)
        if person.x == Person.A:
            pass


class XOR(Gate):
    def __init__(self, person, pre_a, pre_b, next, a, Ma, Ka, b, Mb, Kb):
        """
        :param person:
        :type person Person
        :param pre_a:
        :param pre_b:
        :param next:
        :param a:
        :param Ma:
        :param Ka:
        :param b:
        :param Mb:
        :param Kb:
        """
        super().__init__(person, pre_a, pre_b, next, a, Ma, Ka, b, Mb, Kb)
        # Protocol part 3
        self.y = a ^ b
        self.My = Ma ^ Mb
        self.Ky = Ka ^ Kb
