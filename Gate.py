class Gate:

    TYPE_AND = 0
    TYPE_XOR = 1

    def __init__(self, id, person,  pre_a, pre_b, next):
        self.id = id
        self.pre_a = pre_a
        self.pre_b = pre_b
        self.next = next
        self.person = person
        self.type = None




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
        super().__init__(id, person, pre_a, pre_b, next=None)
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
        super().__init__(id, person, pre_a, pre_b, next=None)
        self.type = Gate.TYPE_XOR
        self.y = None
        self.My = None
        self.Ky = None

   