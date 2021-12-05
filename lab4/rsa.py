from bv import BitReader, BitWriter
import math
import random

def is_prime(a):
    if a < 3: return a == 2
    if not a & 1: return False
    for i in range(3, math.floor(math.sqrt(a))+1, 2):
        if not a % i:
            return False
    return True

def gen_pq():
    seed = random.randint(0, 2**32-1)
    print(seed)
    random.seed(seed)
    def p():
        while not is_prime(p := random.randint(1000,9999)): pass
        return p
    return p(), p()

p, q = gen_pq()
print(p, q)

n = p * q

phi = (p-1) * (q-1)

e = 7


def gcd(a, b):
    while a:
        a, b = b - (b // a) * a, a
    return b



x = is_prime(241)
print(x)

def inv_mod(a, n):
    x, y = 0, 1
    while a:
        q = n // a
        a, n = n - q * a, a
        y, x = x - q * y, y
    return x

def clip(x, n):
    return x - (x // n) * n if x < 0 or x > n else x

e = 0
while not is_prime(e) or gcd(e, phi) != 1:
    e = random.randint(2, phi-1)

e = 211
print("E", e)

d = clip(inv_mod(e, phi), phi)

print("D", d)


# msg = "Wiadomość składająca się z 50-ciu znaków!!!!".encode('utf-8')

msg = "".join([chr(0x41 + i % 26) for i in range(50)]).encode('ascii')
print(msg, len(msg))

import struct
def encode0(msg: bytes, e1, n):
    bl = 2
    l = len(msg)
    pad = bl - (l % bl)
    msg += bytes([0] * pad)
    enc = bytearray()
    for i in range(0, l + pad, bl):
        q =  msg[i:i+bl]
        print(q)
        m = struct.unpack('>H', q)[0]
        if m >= n:
            print(m, ">", n)
        m1 = pow(m, e1, n)
        enc += struct.pack('>H', m1)
    return enc

def codec(msg: bytes, e, n, ibs, obs):
    lm = len(msg) * 8
    l = lm + (ibs - lm % ibs) % ibs
    msg = bytearray(msg) + bytes([0] * math.ceil((l - lm) / 8))

    br = BitReader(msg)
    bw = BitWriter()
    while l - ibs >= 0:
        l -= ibs
        v = br.get(ibs)
        if v > n:
            print("ERR", v, '>', n)
        m = pow(v, e, n)
        bw.put(m, obs)
    if l:
        v = br.get(l)
        m = pow(v, e, n)
        bw.put(m, obs)
        print('2', m)
    return bw.b

def encode(msg, ed, n):
    ks = len(bin(n))-2
    return codec(msg, ed, n, ks-1, ks)

def decode(msg, ed, n):
    ks = len(bin(n))-2
    return codec(msg, ed, n, ks, ks-1)

m = 9


ciph = encode(msg, e, n)
print(ciph.hex())
orig = decode(ciph, d, n)

print(orig)