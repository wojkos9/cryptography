from multiprocessing import shared_memory, Pipe
from multiprocessing.connection import Connection
from os import fork, getpid
import random

n = 179
g = 2

comm_a, comm_b = Pipe(duplex=True)

class Dbg:
    def __init__(self, name, comm):
        self.name = name
        self.comm: Connection = comm

    def log(self, *args, **kwargs):
        print(f"[{self.name}]", *args, **kwargs)

    def send(self, msg):
        self.log("->", msg)
        self.comm.send(msg)

    def recv(self):
        msg = self.comm.recv()
        self.log("recv", msg)
        return msg

def mkagent(name, comm: Connection):
    def agent():
        dbg = Dbg(name, comm)
        x = random.randint(2, n)
        dbg.log(x)

        X = pow(g, x, n)
        dbg.send(X)

        Y = dbg.recv()

        # sync
        comm.send(1)
        comm.recv()

        k = pow(Y, x, n)
        dbg.log(f"k = {Y:3} ^ {x:3} mod {n} = {k}")
    return agent


alice = mkagent("A", comm_a)
bob = mkagent("B", comm_b)

[alice, bob][fork() == 0]()
