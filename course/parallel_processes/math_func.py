"""
Functions:
F1: C := A - B * (MA * MD)
F2: o := Min(MK * MM)
F3: T := (MS * MZ) * (W + X)
"""

from operator import add, mul
from functools import reduce


def make_vector(sz, filler=1):
    return [filler for _ in range(sz)]


def make_sq_matrix(sz, filler=1):
    return make_matrix(sz, sz, filler)


def make_matrix(r, c, filler=1):
    return [[filler for _ in range(c)] for _ in range(r)]


def transpose(m):
    return list(zip(*m))


def vm_mult(v, m):
    return [reduce(add, map(mul, v, c)) for c in transpose(m)]


def mv_mult(m, v):
    return [reduce(add, map(mul, r, v), 0) for r in m]


def mm_mult(ma, mb):
    return [
        [sum(ea*eb for ea, eb in zip(a, b)) for b in transpose(mb)]
        for a in ma
    ]


def v_add(a, b):
    return [ea + eb for ea, eb in zip(a, b)]


def v_subs(a, b):
    return [ea - eb for ea, eb in zip(a, b)]


def func1(a, b, ma, md):
    return v_subs(a, vm_mult(b, mm_mult(ma, md)))


def func2(mk, mm):
    return min(map(min, mm_mult(mk, mm)))


def func3(ms, mz, w, x):
    return mv_mult(mm_mult(ms, mz), v_add(w, x))