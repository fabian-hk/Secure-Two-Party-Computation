import conf
import socket
import sys
from tools.person import Person


class Com:
    TCP_IP = '127.0.0.1'
    TCP_PORT = 1234
    BUFFER_SIZE = 2048

    def __init__(self, person: Person):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if person.x == Person.A:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((self.TCP_IP, self.TCP_PORT))
            self.s.listen(5)
            self.conn, addr = self.s.accept()
            print("Established connection from: " + str(addr))
        if person.x == Person.B:
            self.s.connect((self.TCP_IP, self.TCP_PORT))
            self.conn = self.s
            print("Connection successful")

    def receive(self):
        data = bytes(0)
        while True:
            part = self.conn.recv(self.BUFFER_SIZE)
            data += part
            if len(part) < self.BUFFER_SIZE:
                break
        return data

    def exchange_data(self, id: int, data=bytes(1)):
        print("Com class: send data length: "+str(len(data)))
        self.conn.send(id.to_bytes(1, "big") + data)
        d = self.receive()
        print("Com class: receive data length: " + str(len(d)))
        if d[0] == id:
            return d[1:]

    def close_session(self):
        self.conn.close()
        self.s.close()
