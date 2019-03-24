import os
from random import randint
import conf
import socket
import sys

from tools.person import Person


class Fpre:
    TCP_IP = 'localhost'
    TCP_PORT = 3003
    BUFFER_SIZE = 2048

    def __init__(self, person: Person):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if person.x == Person.A:
            self.s.connect((self.TCP_IP, self.TCP_PORT))
            self.s.send(b'\x00' + person.delta)
            self.receive()
        else:
            self.s.connect((self.TCP_IP, self.TCP_PORT))
            data = self.receive()
            if data[0] == 0:
                person.delta = data[1:]

    def receive(self):
        data = bytes(0)
        while True:
            part = self.s.recv(self.BUFFER_SIZE)
            data += part
            if len(part) < self.BUFFER_SIZE:
                break
        return data

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
        self.s.send(b'\x01' + data)
        self.receive()

    def rec_auth_bits(self):
        """
        Function to receive the finished authenticated bits from the server.
        Method for Person B.
        :return:
        """
        data = self.receive()
        if data[0] == 1:
            return data[1:]

    # ***************** AND triples ********************
    def and_triples(self, data: bytes):
        """
        Sends a single AND triple to the server. For A the server response
        is just b'\x02' and B while receive the third authenticated bit.
        """
        self.s.send(b'\x02' + data)
        d = self.receive()
        if d[0] == 2:
            return d[1:]

    # *********** close current session ***************
    def close_session(self):
        """
        Just for the Fpre server implementation so that the server can be used for multiple sessions.
        """
        self.s.send(b'\xfe')
        self.s.close()
