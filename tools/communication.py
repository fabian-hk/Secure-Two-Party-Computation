import conf
import socket
import sys
from tools.person import Person


class Com:
    TCP_IP = 'localhost'
    TCP_PORT = 1234
    BUFFER_SIZE = conf.k * conf.input_size

    def __init__(self, person: Person):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if person.x == Person.A:
            s.bind((self.TCP_IP, self.TCP_PORT))
            s.listen(5)
            self.conn, addr = s.accept()
            print("Established connection from: " + str(addr))
        if person.x == Person.B:
            s.connect((self.TCP_IP, self.TCP_PORT))
            self.conn = s
            print("Connection successful")

    def receive(self):
        data = bytes(0)
        r = True
        while r:
            part = self.conn.recv(self.BUFFER_SIZE)
            data += part
            if len(part) < self.BUFFER_SIZE:
                r = False
        return data

    def exchange_data(self, id: int, data=bytes(1)):
        self.conn.send(id.to_bytes(1, "big") + data)
        d = self.conn.recv(self.BUFFER_SIZE)
        if d[0] == id:
            return d[1:]
