import socket
import sys
import ssl
from ssl import CertificateError

from tools.person import Person
import conf


class Com:
    BUFFER_SIZE = 2048

    def __init__(self, ip, port, cert, partner, no_encryption=False):
        self.no_encryption = no_encryption

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if not self.no_encryption:
            if cert:
                certificate = conf.crt_storage + cert + '-pub.pem'
                priv_key = conf.crt_storage + cert + '-key.pem'
            else:
                certificate = conf.certificate
                priv_key = conf.priv_key

            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
            context.load_cert_chain(certificate, priv_key)
            context.load_verify_locations(conf.root_cert)
            self.s = context.wrap_socket(s, server_hostname='127.0.0.1')
            self.s.connect((ip, port))
            print("Connection to Fpre successful - " + str(self.s.version()))
        else:
            self.s = s
            self.s.connect((ip, port))
            print("Connection to Fpre successful - no encryption")



        self.receive_buffer = bytes(0)

        data = self.receive()
        if data[0:1] == b'\x00':
            self.person = Person(data[1])
        else:
            sys.exit(1)
        self.id = 0

        ex_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        ex_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ex_s.connect((ip, port + 10))

        if not self.no_encryption:
            if self.person.x == Person.A:
                context_s = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                context_s.verify_mode = ssl.CERT_REQUIRED
                context_s.load_cert_chain(certificate, priv_key)
                context_s.load_verify_locations(conf.crt_storage + 'ca-root.pem')
                self.ex_s = context_s.wrap_socket(ex_s, server_side=True)
                cn = self.get_common_name(self.ex_s.getpeercert())
                if cn != partner:
                    raise CertificateError("hostname '" + partner + "' doesn't match '" + cn + "'")
            else:
                context_c = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context_c.verify_mode = ssl.CERT_REQUIRED
                context_c.check_hostname = True
                context_c.load_cert_chain(certificate, priv_key)
                context_c.load_verify_locations(conf.crt_storage + 'ca-root.pem')
                self.ex_s = context_c.wrap_socket(ex_s, server_hostname=partner)
            print("Connection to exchange successful - " + str(self.ex_s.version()))
        else:
            self.ex_s = ex_s
            print("Connection to exchange successful - no encryption")

        self.ex_receive_buffer = bytes(0)

    @staticmethod
    def get_common_name(certificate):
        for t in certificate['subject']:
            if t[0][0] == "commonName":
                return t[0][1]
        return None

    def receive(self):
        data = self.receive_buffer
        if len(self.receive_buffer) >= 4:
            length = int.from_bytes(data[:4], byteorder='big')
        else:
            data += self.s.recv(self.BUFFER_SIZE)
            length = int.from_bytes(data[:4], byteorder='big')
        data = data[4:]
        while len(data) < length:
            data += self.s.recv(self.BUFFER_SIZE)
        self.receive_buffer = data[length:]
        return data[:length]

    def send_data(self, data):
        self.s.sendall((len(data).to_bytes(4, byteorder='big') + data))

    def ex_receive(self):
        data = self.ex_receive_buffer
        if len(self.ex_receive_buffer) >= 4:
            length = int.from_bytes(data[:4], byteorder='big')
        else:
            data += self.ex_s.recv(self.BUFFER_SIZE)
            length = int.from_bytes(data[:4], byteorder='big')
        data = data[4:]
        while len(data) < length:
            data += self.ex_s.recv(self.BUFFER_SIZE)
        self.ex_receive_buffer = data[length:]
        return data[:length]

    def ex_send_data(self, data):
        self.ex_s.sendall((len(data).to_bytes(4, byteorder='big') + data))

    def exchange_data(self, data=bytes(1)):
        self.ex_send_data(self.id.to_bytes(4, "big") + data)
        d = self.ex_receive()
        if int.from_bytes(d[:4], byteorder='big') == self.id:
            self.id += 1
            return d[4:]
        else:
            print("Com class error ID not equal")

    def close_session(self):
        self.send_data(b'\xfe')
        self.s.close()

        if not self.no_encryption:
            self.ex_s = self.ex_s.unwrap()
        self.ex_s.sendall(b'\xfe')
        self.ex_s.close()
