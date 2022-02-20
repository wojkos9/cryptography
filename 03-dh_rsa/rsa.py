from bitvector import BitReader, BitWriter
import math
import random

def is_prime(a):
    if a < 3: return a == 2
    if not a & 1: return False
    for i in range(3, math.floor(math.sqrt(a))+1, 2):
        if not a % i:
            return False
    return True

def gcd(a, b):
    while a:
        a, b = b - (b // a) * a, a
    return b

def inv_mod(a, n):
    x, y = 0, 1
    while a:
        q = n // a
        a, n = n - q * a, a
        y, x = x - q * y, y
    return x

def clip(x, n):
    return x - (x // n) * n if x < 0 or x > n else x

def rsa_codec(msg: bytes, e, n, ibs, obs):
    l = len(msg) * 8
    br = BitReader(msg)
    bw = BitWriter()
    while l - ibs >= 0:
        l -= ibs
        v = br.get(ibs)
        m = pow(v, e, n)
        bw.put(m, obs)
    if l:
        v = br.get(l)
        m = pow(v, e, n)
        bw.put(m, obs)
    return bw.getbuf()

def rsa_pad_msg(msg, bs):
    lm = len(msg) * 8
    l = lm + (bs - lm % bs) % bs
    return bytes(msg) + bytes([0] * math.ceil((l - lm) / 8))

def rsa_encode(msg, ed, n):
    ks = len(bin(n))-2
    msg1 = rsa_pad_msg(msg, ks-1)
    return rsa_codec(msg1, ed, n, ks-1, ks)

def rsa_decode(msg, ed, n):
    ks = len(bin(n))-2
    return rsa_codec(msg, ed, n, ks, ks-1)

def gen_pq():
    seed = random.randint(0, 2**32-1)
    print("Seed:", seed)
    random.seed(seed)
    def p():
        while not is_prime(p := random.randint(1000,9999)): pass
        return p
    return p(), p()

if __name__ == "__main__":
    p, q = gen_pq()
    n = p * q
    phi = (p-1) * (q-1)
    print(f'p = {p}, q = {q}, n = {n}, phi = {phi}')

    e = 0
    while not is_prime(e) or gcd(e, phi) != 1:
        e = random.randint(2, phi-1)
    print("e =", e)

    d = clip(inv_mod(e, phi), phi)
    print("d =", d)

    print("\nPublic key: ", (e, n))
    print("Private key:", (d, n))

    msg = "".join([chr(0x41 + i % 26) for i in range(50)])
    msg_bytes = msg.encode('ascii')
    print("\nMessage:", msg, "\n")

    print(f"Encrypt using e={e}, n={n}...")
    ciph = rsa_encode(msg_bytes, e, n)
    print("Encrypted:", ciph.hex(), "\n")

    print(f"Decrypt using d={d}, n={n}...")
    orig = rsa_decode(ciph, d, n)
    orig_str = orig.decode('ascii')
    print("Decrypted:", orig_str)
