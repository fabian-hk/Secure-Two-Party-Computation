def xor(a, b, c=bytearray(0), d=bytearray(0)):
    """
    :param a:
    :param b:
    :param c:
    :param d:
    :return c: element wise xor of a and b
    :rtype bytearray
    """
    l = max(len(a), len(b), len(c), len(d))
    # do padding if the variables doesn't have the same length
    if len(a) < l:
        a = bytearray(l - len(a)) + a
    if len(b) < l:
        b = bytearray(l - len(b)) + b
    if len(c) < l:
        c = bytearray(l - len(c)) + c
    if len(d) < l:
        d = bytearray(l - len(d)) + d

    e = bytearray(l)
    for i in range(l):
        e[i] = a[i] ^ b[i] ^ c[i] ^ d[i]
    return e
