def xor(a: bytearray, b: bytearray, c=bytearray(0), d=bytearray(0), e=bytearray(0)) -> bytearray:
    """
    :param a:
    :param b:
    :param c:
    :param d:
    :param e:
    :return f: bit wise xor of a and b
    :rtype bytearray
    """
    l = max(len(a), len(b), len(c), len(d))
    # do padding with 0 if the variables doesn't have the same length
    if len(a) < l:
        a = bytearray(l - len(a)) + a
    if len(b) < l:
        b = bytearray(l - len(b)) + b
    if len(c) < l:
        c = bytearray(l - len(c)) + c
    if len(d) < l:
        d = bytearray(l - len(d)) + d
    if len(e) < l:
        e = bytearray(l - len(e)) + e

    f = bytearray(l)
    for i in range(l):
        f[i] = a[i] ^ b[i] ^ c[i] ^ d[i] ^ e[i]
    return f


def AND(a, b):
    """
    :param a:
    :param b:
    :return c: bit wise and of a and b
    :rtype bytearray
    """
    l = max(len(a), len(b))
    # do padding with 0 if the variables doesn't have the same length
    if len(a) < l:
        a = bytearray(l - len(a)) + a
    if len(b) < l:
        b = bytearray(l - len(b)) + b
    c = bytearray(l)
    for i in range(l):
        c[i] = a[i] & b[i]
    return c


def check_and_triple(and_triple_A, and_triple_B, delta_a: bytes, delta_b: bytes):
    """
    Checks two AND triples if they are corrct
    :param and_triple_A: first AND triple as protobuf message
    :param and_triple_B:  second AND triple as protobuf message
    :param delta_a: delta from person A as bytes
    :param delta_b: delta from person B as bytes
    """
    # check first bit from A
    if and_triple_A.r1 == b'\x01':
        if and_triple_A.M1 == bytes(xor(and_triple_B.K1, delta_b)):
            pass
            # print("Correct bit 1 A. ID: " + str(and_triple_A.id))
        else:
            print(and_triple_A)
            print(and_triple_B)
            print("Cheat bit 1 A. ID: " + str(and_triple_A.id))
    else:
        if and_triple_A.M1 == and_triple_B.K1:
            pass
            # print("Correct bit 1 A. ID: " + str(and_triple_A.id))
        else:
            print(and_triple_A)
            print(and_triple_B)
            print("Cheat bit 1 A. ID: " + str(and_triple_A.id))

    # check second bit A
    if and_triple_A.r2 == b'\x01':
        if and_triple_A.M2 == bytes(xor(and_triple_B.K2, delta_b)):
            pass
            # print("Correct bit 2 A. ID: " + str(and_triple_A.id))
        else:
            print(and_triple_A)
            print(and_triple_B)
            print("Cheat bit 2 A. ID: " + str(and_triple_A.id))
    else:
        if and_triple_A.M2 == and_triple_B.K2:
            pass
            # print("Correct bit 2 A. ID: " + str(and_triple_A.id))
        else:
            print(and_triple_A)
            print(and_triple_B)
            print("Cheat bit 2 A. ID: " + str(and_triple_A.id))

    # check first bit from B
    if and_triple_B.r1 == b'\x01':
        if and_triple_B.M1 == bytes(xor(and_triple_A.K1, delta_a)):
            pass
            # print("Correct bit 1 B. ID: " + str(and_triple_B.id))
        else:
            print(and_triple_A)
            print(and_triple_B)
            print("Cheat bit 1 B. ID: " + str(and_triple_B.id))
    else:
        if and_triple_B.M1 == and_triple_A.K1:
            pass
            # print("Correct bit 1 B. ID: " + str(and_triple_B.id))
        else:
            print(and_triple_A)
            print(and_triple_B)
            print("Cheat bit 1 B. ID: " + str(and_triple_B.id))

    # check second bit B
    if and_triple_B.r2 == b'\x01':
        if and_triple_B.M2 == bytes(xor(and_triple_A.K2, delta_a)):
            pass
            # print("Correct bit 2 B. ID: " + str(and_triple_B.id))
        else:
            print(and_triple_A)
            print(and_triple_B)
            print("Cheat bit 2 B. ID: " + str(and_triple_B.id))
    else:
        if and_triple_B.M2 == and_triple_A.K2:
            pass
            # print("Correct bit 2 B. ID: " + str(and_triple_B.id))
        else:
            print(and_triple_A)
            print(and_triple_B)
            print("Cheat bit 2 B. ID: " + str(and_triple_B.id))
