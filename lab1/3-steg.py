import os
import numpy as np
from skimage import io
import struct


DIR = os.path.dirname(os.path.realpath(__file__))
img = io.imread(f"{DIR}/lena.png")

msg = "Hello, this is a secret message!!!"

# Encodes a message in an image, prepended by 32 bits of message length
def steg_enc(img: np.ndarray, msg: bytes):
    sh = img.shape
    new = img.flatten()
    data = bytearray(struct.pack("<I", len(msg)))
    data += msg

    i = 0
    p2 = [2**x for x in range(7, -1, -1)]
    for b in data:
        for j in p2:
            old = new[i]
            bit = 1 if b & j else 0
            new[i] = (old & 0xfe) | bit
            i += 1

    return new.reshape(sh)

def dec_n_bytes(gen, n):
        lim = n * 8
        ans = [0] * n
        cur = 0
        j = 0
        for i, b in enumerate(gen):
            cur = cur << 1 | (b & 1)

            if i % 8 == 7:
                ans[j] = cur
                cur = 0
                j += 1

            if i == lim - 1:
                break

        return bytes(ans)


def steg_dec(img: np.ndarray):
    gen = (b for b in img.reshape((-1,)))
    size = struct.unpack("<I", dec_n_bytes(gen, 4))[0]
    print(size)
    return dec_n_bytes(gen, size)


with_secret = steg_enc(img, msg.encode('ascii'))

secret = steg_dec(with_secret)

print(secret)
