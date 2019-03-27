import os
from random import randint
import socket
import conf
import sys



from tools.person import Person


class Fpre:
    TCP_IP = 'localhost'
    TCP_PORT = 3003
    BUFFER_SIZE = int((conf.k / 2) * (conf.upper_bound_gates * 3))

    def __init__(self, person: Person):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if person.x == Person.A:
            self.s.connect((self.TCP_IP, self.TCP_PORT))
            self.s.send(b'\x00' + person.delta)
            self.s.recv(self.BUFFER_SIZE)
        else:
            self.s.connect((self.TCP_IP, self.TCP_PORT))
            data = self.s.recv(self.BUFFER_SIZE)
            if data[0] == 0:
                person.delta = data[1:]

    # ********** create authenticated bits *************
    @staticmethod
    def authenticated_bit(auth_bit=None):
        """
        Creates a single bit r, a Tag M and a Key K. These can be used to
        send to the Fpre server so it can create a complete authenticated bit.
        """
        r = randint(0, 1)
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
        self.s.send(b'\x01' + data)
        self.s.recv(self.BUFFER_SIZE)

    def rec_auth_bits(self):
        """
        Function to receive the finished authenticated bits from the server.
        Method for Person B.
        :return:
        """
        data = self.s.recv(self.BUFFER_SIZE)
        if data[0] == 1:
            return data[1:]

    # ***************** AND triples ********************
    def and_triples(self, data: bytes):
        """
        Sends a single AND triple to the server. For A the server response
        is just b'\x02' and B while receive the third authenticated bit.
        """
        self.s.send(b'\x02' + data)
        return_data = self.s.recv(self.BUFFER_SIZE)
        if return_data[0] == 2:
            return return_data[1:]

    # *********** close current session ***************
    def close_session(self):
        """
        Just for the Fpre server implementation so that the server can be used for multiple sessions.
        """
        self.s.send(b'\xfe')
        self.s.close()
