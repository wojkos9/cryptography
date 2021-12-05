def botm(n):
    return ((1 << n) - 1)
def topm(n):
    return ((1 << n) - 1) << (8-n)

class OverreadException(Exception):
    pass

class BitReader:
    def __init__(self, b: bytes):
        self.b = b
        self.bn = 0
        self.i = 0

    def get(self, n) -> str:
        r = 0
        if self.bn + n // 8 + (1 if (n%8+self.i) > 7 else 0) > len(self.b):
            raise OverreadException()
        if self.i:
            k = 8 - self.i
            t = min(k, n)
            r = self.b[self.bn] & topm(t) >> self.i
            if k == t:
                self.bn += 1
                self.i = 0
            else:
                self.i += t
                r >>= (k-t)
            n -= t
        if n:
            e = n // 8
            for i in range(self.bn, self.bn + e):
                r = (r << 8) + self.b[i]
            n -= e * 8
            self.bn += e
            if n:
                r = (r << n) ^ (self.b[self.bn] & topm(n)) >> (8-n)
                self.i += n
        return r

class BitWriter:
    def __init__(self):
        self.b = bytearray([])
        self.x = ''
        self.tl = 0

    def put(self, v, n, mode=0):
        s = bin(v)[2:]
        if len(s) > n:
            raise Exception()
        s = s.zfill(n) if mode == 0 else s + '0' * (n-len(s))
        if self.x:
            self.b.pop()
        x = self.x + s
        lx = len(x)
        for i in range(0, lx-8+1, 8):
            f = x[i:i+8]
            self.b.append(int(f, 2))
        m = lx % 8
        if m:
            x = x[-m:]
            self.b.append(int(x, 2) << (8-m))
            self.x = x
        else:
            self.x = ''
        self.tl += n

    def str(self):
        return bufs(self.b)

def bufs(buf, sep=""):
    return sep.join(bin(x)[2:].zfill(8) for x in buf)

def bufx(buf, sep=""):
    return sep.join(hex(x)[2:].zfill(2) for x in buf)

import random
def test_br():
    n = 16
    bn = n * 8
    bn0 = bn
    maxb = 32
    buf = random.randbytes(n)
    br = BitReader(buf)
    s = bufs(buf)
    i = 0
    slices = []
    while bn - (k := random.randint(1, maxb)) >= 0:
        bn -= k
        slices.append(k)
    if bn:
        slices.append(bn)
    for k in slices:
        a = bin(br.get(k))[2:].zfill(k)
        b = s[i:i+k]
        if a != b:
            raise Exception(f"Test failed: {a}!={b} {i}:{i+k}/{bn0}")
        i += k

def test_bw():
    bw = BitWriter()
    s = ""
    tl = 0
    for _ in range(10):
        a = random.randint(0, 2**16)
        b = random.randint(0, 5)
        ba = bin(a)[2:]
        l = len(ba) + b
        tl += l
        c = ba.zfill(l)
        bw.put(a, l)
        s += c
        z = bufs(bw.b)[:tl]
        print("OK" if s == z else "NO", a, l, bin(a)[2:].zfill(l))
        if s != z:
            break
