from functools import reduce
import random
from fractions import Fraction

def frac(f):
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def polynomial(coef):
    x2n = lambda n: "" if n == 0 else ("x" if n == 1 else f"x^{n}")
    return "f(x) = " + " + ".join(
            f"{a_n}{x2n(i)}"
            for (a_n, i) in zip(coef, range(len(coef)))
        )

def print_iter(fmt, vals):
    print(*(fmt % v for v in vals), sep="\n", end="\n\n")

prod = lambda xx: reduce(int.__mul__, xx)

def shamir_split(n, t, s, p, verbose=True, aa=None):
    if not aa:
        aa = [random.randint(2, p) for _ in range(t-1)]
    a = [s, *aa] #*aa[:t-1]]

    if verbose:
        print_iter("%10s: %d", (
            ("Fragments", n),
            ("Required", t),
            ("Secret", s),
            ("Prime", p)
        ))
        print(f"Polynomial: {polynomial(a)}\n")

    f = lambda x: sum(
            a_n * pow(x, i, p)
            for (a_n, i) in zip(a, range(n-1))
        ) % p

    xx = list(range(1, n+1))
    yy = [f(i) for i in xx]

    return list(zip(xx, yy))



def shamir_reconstruct(shares, p, verbose=True):
    t = len(shares)
    sx, sy = zip(*shares)

    if verbose:
        print("Shares:")
        print_iter("(x%d, y%d) = (%d, %d)", ((i, i, sh[0], sh[1]) for i, sh in enumerate(shares)))


    l_const_term = lambda i: Fraction(
            prod((      - sx[j] for j in range(t) if i != j)),
            prod((sx[i] - sx[j] for j in range(t) if i != j))
        )

    lc = [l_const_term(i) for i in range(t)]

    if verbose:
        print("Constant terms:")
        print_iter("l%d_0 = %s", ((i, frac(lc[i])) for i in range(t)))

    print(sy)
    tt = [y*l for (y,l) in zip(sy, lc)]
    print(*[frac(t) for t in tt], sep=" + ")
    return sum(tt) % p

def demo():
    random.seed(1337)
    n = 6
    t = 3
    s = 1234
    p = 1523

    all_shares = shamir_split(n, t, s, p, aa=[166, 94])

    # shares = sorted(random.sample(all_shares, k=t))
    shares = [all_shares[i] for i in (1, 3, 4)]
    secret = shamir_reconstruct(shares, p)

    print(f"Secret: {secret}")

if __name__ == "__main__":
    demo()