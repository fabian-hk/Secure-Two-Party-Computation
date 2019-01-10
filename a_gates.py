class Gate:
    def __init__(self, pre_a, pre_b, next, a, Ma, Ka, b, Mb, Kb, y=[], My=[], Ky=[]):
        self.a = a
        self.Ma = Ma
        self.Ka = Ka
        self.b = b
        self.Mb = Mb
        self.Kb = Kb
        self.y = y
        self.My = My
        self.Ky = Ky

        self.pre_a = pre_a
        self.pre_b = pre_b
        self.next = next


class AND(Gate):
    def __init__(self, pre_a, pre_b, next, a, Ma, Ka, b, Mb, Kb):
        super().__init__(pre_a, pre_b, next, a, Ma, Ka, b, Mb, Kb)


class XOR(Gate):
    def __init__(self, pre_a, pre_b, next, a, Ma, Ka, b, Mb, Kb):
        # Protocol part 3
        y = a ^ b
        My = Ma ^ Mb
        Ky = Ka ^ Kb
        super().__init__(pre_a, pre_b, next, a, Ma, Ka, b, Mb, Kb, y, My, Ky)
