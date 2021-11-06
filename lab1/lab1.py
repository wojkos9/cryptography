from functools import reduce
from random import randint, seed
n = 4
t = 3
s = 954
p = 1523

seed(1337)

def str_poly(coef):
    x2n = lambda n: "" if n == 0 else ("x" if n == 1 else f"x^{n}")
    return "f(x) = " + " + ".join(
            f"{a_n}{x2n(i)}"
            for (a_n, i) in zip(coef, range(len(coef)-1, -1, -1))
        )

def iter_print(fmt, vals):
    print(*(fmt % v for v in vals), sep="\n", end="\n\n")

product = lambda xx: reduce(int.__mul__, xx)

def do_shamir(n, t, s, p, verbose=True):
    aa = [62, 352, 123]
    a = [*aa[:t-1], s]

    if verbose:
        iter_print("%10s: %d", (
            ("Fragments", n),
            ("Required", t),
            ("Secret", s),
            ("Prime", p)
        ))
        print(f"Polynomial: {str_poly(a)}\n")

    f = lambda x: sum(
            a_n * pow(x, i, p)
            for (a_n, i) in zip(reversed(a), range(n-1))
        ) % p

    xx = [randint(1, p-1) for _ in range(t)] #range(2, 2+t)
    yy = [f(i) for i in xx]

    if verbose:
        iter_print("(x%d, y%d) = (%d, %d)", ((i, i, xx[i], yy[i]) for i in range(t)))



    l_const_term = lambda i: (
            product((      - xx[j] for j in range(t) if i != j)) //
            product((xx[i] - xx[j] for j in range(t) if i != j))
        )

    ll = [l_const_term(i) for i in range(t)]

    if verbose:
        iter_print("L0_%d = %d", ((i, ll[i]) for i in range(t)))

    tt = [y*l % p for (y,l) in zip(yy, ll)]
    print(tt)
    return sum(tt) % p

sol = do_shamir(n, t, s, p)

print(f"SOL: {sol}")