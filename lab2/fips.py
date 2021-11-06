def count1(barr):
    return sum(bin(x).count("1") for x in barr)

def fips1(k):
    v = count1(k)
    return 9725 < v < 10275

def fips2(k):
    v = [0] * 6
    ranges = (
        (2315, 2685),
        (1114, 1386),
        (527,  723),
        (240,  384),
        (103,  209),
        (103,  209)
    )
    s = 0
    max_s = 0
    for b in k:
        t = 0x80
        while t:
            if b & t:
                s += 1
            elif s:
                max_s = max(s, max_s)
                v[min(s, 6)-1] += 1
                s = 0
            t >>= 1
    ans = [a < x < b for (x, (a, b)) in zip(v, ranges)]
    return all(ans)

def fips3(k):
    s = 0
    max_0 = 0
    max_1 = 0
    ones = k[0] & 0x80
    for b in k:
        t = 0x80
        while t:
            bset = b & t
            if ones:
                if bset:
                    s += 1
                else:
                    max_1 = max(s, max_1)
                    ones = False
                    s = 1
            else:
                if bset:
                    max_0 = max(s, max_0)
                    ones = True
                    s = 1
                else:
                    s += 1
            t >>= 1
    if ones:
        max_1 = max(s, max_1)
    else:
        max_0 = max(s, max_0)

    return max_0 < 26 and max_1 < 26

def fips4(k):
    v = [0] * 16
    for b in k:
        v[b >> 4] += 1
        v[b & 15] += 1

    X = 16 / 5000 * sum(si ** 2 for si in v) - 5000
    return 2.16 < X < 46.17

fips_140_2 = (fips1, fips2, fips3, fips4)