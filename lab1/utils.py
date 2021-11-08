from fractions import Fraction

def to_int_mod(f: Fraction, p):
    n, d = f.numerator, f.denominator
    if d == 1:
        return n % p
    elif p % d == 0:
        return n / d % p
    n1 = n
    while n1 % d:
        n1 += p
    r = (n1 // d) % p
    return r

def ellipsis(msg, show_len=20):
    msg = repr(msg)
    if len(msg) <= show_len * 2:
        return msg
    return msg[:show_len] + "..." + msg[-show_len:]