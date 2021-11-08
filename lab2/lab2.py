import random
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path + "/primes.txt", "r") as f:
    p, q = [int(n) for n in f.read().split(" ")[:2]]

N = p * q

def genkey(l):
    while (x := random.randint(2, N-1)) in [p, q]:
        pass
    k = bytearray()
    while l > 0:
        nbyte = 0
        for _ in range(min(l, 8)):
            x = pow(x, 2, N)
            nbyte = nbyte << 1 | (x & 1)
        if l < 8:
            nbyte <<= l - 8
            l = 0
        else:
            l -= 8
        k.append(nbyte)

    return k

def genkey_if_needed(m = 20000):
    global k
    KEYFILE = dir_path + "/key.bin"

    if os.path.exists(KEYFILE) and not FORCE_GEN:
        with open(KEYFILE, "rb") as f:
            k = f.read()
    else:
        print(f"Generating new {m}-bit key...")
        k = genkey(m)
        with open(KEYFILE, "wb") as f:
            f.write(k)

random.seed(1337)
FORCE_GEN = True

genkey_if_needed()

from fips import fips_140_2

res = [fips(k) for fips in fips_140_2]

khex = k.hex()
print("KEY:", khex if len(khex) <= 16 else f"{khex[:8]}...{khex[-8:]}")

for t,r in zip(fips_140_2, res):
    print(f"{t.__name__}: {r}")

print("random?:", all(res))
