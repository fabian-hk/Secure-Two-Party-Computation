import os
from random import randint

import conf
from tools.person import Person
from tools.communication import Com


class Fpre(Com):

    def __init__(self, ip, port):
        super().__init__(ip, port)

    def init_fpre(self):
        if self.person.x == Person.A:
            self.send_data(b'\x01' + self.person.delta)
            self.receive()
        else:
            data = self.receive()
            if data[0] == 1:
                self.person.delta = data[1:]

    # ********** create authenticated bits *************
    @staticmethod
    def authenticated_bit(auth_bit=None):
        """
        Creates a single bit r, a Tag M and a Key K. These can be used to
        send to the Fpre server so it can create a complete authenticated bit.
        """
        r = randint(0, 1)  # TODO change to os.urandom() for more safety??
        M = os.urandom(int(conf.k / 8))
        K = os.urandom(int(conf.k / 8))
        if auth_bit:
            auth_bit.r = r.to_bytes(1, "big")
            auth_bit.M = M
            auth_bit.K = K
        return r.to_bytes(1, "big"), M, K

    def send_auth_bits(self, data):
        """
        Sends all bits encoded as bytes to the server so it can create
        complete authenticated bits. Method for Person A.
        :param data:
        """
        self.send_data(b'\x02' + data)
        self.receive()

    def rec_auth_bits(self):
        """
        Function to receive the finished authenticated bits from the server.
        Method for Person B.
        :return:
        """
        data = self.receive()
        if data[0] == 2:
            return data[1:]

    # ***************** AND triples ********************
    def and_triples(self, data: bytes):
        """
        Sends a single AND triple to the server. For A the server response
        is just b'\x03' and B while receive the third authenticated bit.
        """
        self.send_data(b'\x03' + data)
        d = self.receive()
        if d[0] == 3:
            return d[1:]
