def xor(a, b, c=None, d=None):
    """
    :param a:
    :param b:
    :param c:
    :param d:
    :return c: element wise xor of a and b
    :rtype bytearray
    """
    if len(a) != len(b):
        raise Exception("Byte objects doesn't have the same length")
    if not c:
        c = bytearray(len(a))
    if not d:
        d = bytearray(len(a))
    e = bytearray(len(a))
    for i in range(len(a)):
        e[i] = a[i] ^ b[i] ^ c[i] ^ d[i]
    return e
