from functools import reduce
import random
from fractions import Fraction
import argparse
from utils import to_int_mod

def frac(f):
    return str(f) if not isinstance(f, Fraction) else (str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}")

def polynomial(coef):
    x2n = lambda n: "" if n == 0 else ("x" if n == 1 else f"x^{n}")
    return "f(x) = " + " + ".join(
            f"{a_n}{x2n(i)}"
            for (a_n, i) in zip(coef, range(len(coef)))
        )

def print_iter(fmt, vals):
    print(*(fmt % v for v in vals), sep="\n", end="\n\n")

def print_shares(shares):
    print_iter("(x%d, y%d) = (%d, %d)", ((i, i, sh[0], sh[1]) for i, sh in enumerate(shares)))

prod = lambda xx: reduce(int.__mul__, xx)

def shamir_split(n, t, s, p, verbose=True, aa=None):
    if not aa:
        aa = [random.randint(2, p) for _ in range(t-1)]
    a = [s, *aa[:t-1]]

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
        print("Chosen shares:")
        print_shares(shares)

    l_const_term = lambda i: Fraction(
            prod((      - sx[j] for j in range(t) if i != j)),
            prod((sx[i] - sx[j] for j in range(t) if i != j))
        )

    lc = [l_const_term(i) for i in range(t)]

    if verbose:
        print("Constant terms:")
        print_iter("l%d_0 = %s", ((i, frac(lc[i])) for i in range(t)))

    tt = [to_int_mod(y*l, p) for (y,l) in zip(sy, lc)]
    return sum(tt) % p

def demo():
    random.seed(1337)

    par = argparse.ArgumentParser()
    par.add_argument('-n', type=int, help='number of shares', default=4)
    par.add_argument('-t', type=int, help='number of shares required', default=3)
    par.add_argument('-s', type=int, help='secret', default=954)
    par.add_argument('-p', type=int, help='prime', default=1523)
    par.add_argument('-a', nargs='+', type=int, help='polynomial coefficients')
    par.add_argument('-A', action='store_const', help='use default polynomial coefficients', const=[352, 62])
    par.add_argument('-r', nargs='+', type=str, help='shares to reconstruct from')
    par.add_argument('-g', action='store_true', help='only generate shares')

    args = par.parse_args()

    n = args.n
    t = args.t
    s = args.s
    p = args.p
    aa = args.a if args.a else args.A

    if args.g or not args.r:
        all_shares = shamir_split(n, t, s, p, aa=aa)
        print("All shares:")
        print_shares(all_shares)
        print(*(f"{x},{y}" for x,y in all_shares), end="\n\n")
        if args.g:
            return


    if args.r:
        shares = [tuple([int(x) for x in y.split(",")]) for y in args.r]
    else:
        shares = sorted(random.sample(all_shares, k=t)) if not args.r else args.r


    # shares = [all_shares[i] for i in (1, 3, 4)]
    secret = shamir_reconstruct(shares, p)

    print(f"Secret: {secret}")

if __name__ == "__main__":
    demo()
