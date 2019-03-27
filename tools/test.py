import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
import struct

# AES encryption and decryption
backend = default_backend()
k1 = os.urandom(16)
k2 = os.urandom(16)
iv = os.urandom(16)
print(iv)
cipher = Cipher(algorithms.AES(k1+k2), modes.CBC(iv), backend=backend)
encryptor = cipher.encryptor()
ct = encryptor.update(b"Hello World!!!!!Hello World!!!!!") +  encryptor.finalize()
print("AES encrypted text:")
print(ct)

decryptor = cipher.decryptor()
plain = decryptor.update(ct) + decryptor.finalize()
print("Encrypted text:")
print(plain)

# use of a hash function
h = hashlib.sha3_256()
h.update(int.to_bytes(340282366920938463, length=16, byteorder='big'))
print("SHA3-512 Hash:")
print(bytearray(h.digest()))