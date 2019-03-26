import socket
from multiprocessing import Process

from fpre.fpre_server import FpreServer


class Server(Process):
    TCP_IP = 'localhost'

    def __init__(self, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.TCP_IP, port))
        self.s.listen(5)

    def start_server(self):
        """
        Runs server in the same process as it was instantiated.
        """
        while True:
            print("Waiting for connection")

            conn1, addr1 = self.s.accept()
            print("First connection. IP: " + str(addr1))

            conn2, addr2 = self.s.accept()
            print("Second connection. IP: " + str(addr2))

            print()

            conn = Connection(conn1, conn2)
            conn.start()

    def run(self):
        """
        Runs server in a new process.
        """
        self.start_server()


class Connection(Process):
    BUFFER_SIZE = 2048

    def __init__(self, conn1: socket, conn2: socket):
        super().__init__()
        self.conn1 = conn1
        self.conn2 = conn2

        self.fpre_server = FpreServer()

    def receive(self, conn):
        data = bytes(0)
        while True:
            part = conn.recv(self.BUFFER_SIZE)
            data += part
            if len(part) < self.BUFFER_SIZE:
                break
        return data

    def run(self):
        # initialize connection with the appropriate persons
        self.conn1.sendall(b'\x00\x00')
        self.conn2.sendall(b'\x00\x01')

        run = True
        while run:
            data_A = self.receive(self.conn1)
            if not data_A:
                continue

            if data_A[0:1] == b'\x01':
                delta_b = self.fpre_server.init(data_A[1:])
                self.conn2.sendall(b'\x01' + delta_b)
                self.conn1.sendall(b'\x01')
            elif data_A[0:1] == b'\x02':
                ser_auth_bits_b = self.fpre_server.create_auth_bits(data_A[1:])
                self.conn2.sendall(b'\x02' + ser_auth_bits_b)
                self.conn1.sendall(b'\x02')
            elif data_A[0:1] == b'\x03':
                data_B = self.receive(self.conn2)
                if data_B[0:1] == b'\x03':
                    ser_and_triple_b = self.fpre_server.create_and_triple(data_A[1:], data_B[1:])
                    self.conn2.sendall(b'\x03' + ser_and_triple_b)
                    self.conn1.sendall(b'\x03')
                else:
                    print("Data_B not 2")
            elif data_A[0:1] == b'\xfd':
                data_B = self.receive(self.conn2)
                self.conn1.sendall(data_B[1:])
                self.conn2.sendall(data_A[1:])
            elif data_A == b'\xfe':
                self.conn1.shutdown(socket.SHUT_RDWR)
                self.conn1.close()
                self.conn2.shutdown(socket.SHUT_RDWR)
                self.conn2.close()
                run = False



