import socket
from multiprocessing import Process
import ssl
import select

from fpre.fpre_server import FpreServer
import conf


class Server(Process):

    def __init__(self, port):
        super().__init__()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', port))
        self.s.listen(5)
        # TODO wrap socket at this point already

        self.ex_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.ex_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ex_s.bind(('', port + 10))
        self.ex_s.listen(5)

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

            conn = Connection(conn1, conn2)
            conn.start()

            conn3, addr3 = self.ex_s.accept()
            print("Third connection. IP: " + str(addr3))

            conn4, addr4 = self.ex_s.accept()
            print("Fourth connection. IP: " + str(addr4))

            print()

            ex = Exchange(conn3, conn4)
            ex.start()

    def run(self):
        """
        Runs server in a new process.
        """
        self.start_server()


class Exchange(Process):
    BUFFER_SIZE = 4096

    def __init__(self, conn1, conn2):
        super().__init__()
        self.conn1 = conn1
        self.conn2 = conn2
        self.conn1.setblocking(0)
        self.conn2.setblocking(0)

        self.receive_buffer = bytes(0)

    def run(self):
        run = True
        while run:
            readable_s, _, _ = select.select([self.conn1, self.conn2], [], [])

            for sock in readable_s:
                data = sock.recv(self.BUFFER_SIZE)
                if data != b'\xfe':
                    if sock == self.conn1:
                        self.conn2.sendall(data)
                    elif sock == self.conn2:
                        self.conn1.sendall(data)
                else:
                    run = False

        self.conn1.shutdown(socket.SHUT_RDWR)
        self.conn1.close()
        self.conn2.shutdown(socket.SHUT_RDWR)
        self.conn2.close()


class Connection(Process):
    BUFFER_SIZE = 2048

    def __init__(self, conn1: socket, conn2: socket):
        super().__init__()

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(conf.crt_storage + 'certificate-localhost-pub.pem',
                                conf.crt_storage + 'certificate-localhost-key.pem')

        self.conn1 = context.wrap_socket(conn1, server_side=True)
        self.conn2 = context.wrap_socket(conn2, server_side=True)

        self.receive_buffer = bytes(0)

        self.fpre_server = FpreServer()

    def receive(self, conn):
        data = self.receive_buffer
        data += conn.recv(self.BUFFER_SIZE)
        length = int.from_bytes(data[:4], byteorder='big')
        data = data[4:]
        while len(data) < length:
            data += conn.recv(self.BUFFER_SIZE)
        self.receive_buffer = data[length:]
        return data[:length]

    def send_data(self, conn, data):
        conn.sendall((len(data).to_bytes(4, byteorder='big') + data))

    def run(self):
        # initialize connection with the appropriate persons
        self.send_data(self.conn1, b'\x00\x00')
        self.send_data(self.conn2, b'\x00\x01')

        run = True
        while run:
            data_A = self.receive(self.conn1)
            if not data_A:
                continue

            if data_A[0:1] == b'\x01':
                delta_b = self.fpre_server.init(data_A[1:])
                self.send_data(self.conn2, b'\x01' + delta_b)
                self.send_data(self.conn1, b'\x01')
            elif data_A[0:1] == b'\x02':
                ser_auth_bits_b = self.fpre_server.create_auth_bits(data_A[1:])
                self.send_data(self.conn2, b'\x02' + ser_auth_bits_b)
                self.send_data(self.conn1, b'\x02')
            elif data_A[0:1] == b'\x03':
                print("Created AND triple")
                data_B = self.receive(self.conn2)
                if data_B[0:1] == b'\x03':
                    ser_and_triple_b = self.fpre_server.create_and_triple(data_A[1:], data_B[1:])
                    self.send_data(self.conn2, b'\x03' + ser_and_triple_b)
                    self.send_data(self.conn1, b'\x03')
                else:
                    print("Data_B not 2")
            elif data_A[0:1] == b'\xfd':
                data_B = self.receive(self.conn2)
                self.send_data(self.conn1, data_B[1:])
                self.send_data(self.conn2, data_A[1:])
            elif data_A == b'\xfe':
                self.conn1.shutdown(socket.SHUT_RDWR)
                self.conn1.close()
                self.conn2.shutdown(socket.SHUT_RDWR)
                self.conn2.close()
                run = False


if __name__ == "__main__":
    server = Server(8448)
    server.start_server()
