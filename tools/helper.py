def xor(a, b, c=bytearray(0), d=bytearray(0), e=bytearray(0)):
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
        f[i] = a[i] ^ b[i] ^ c[i] ^ d[i]
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
