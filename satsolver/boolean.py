#!/usr/bin/python

class Formula:
    def __and__(self, other):
        return And(self, other)

    def __rand__(self, other):
        return And(other, self)

    def __or__(self, other):
        return Or(self, other)

    def __ror__(self, other):
        return Or(other, self)

    def __xor__(self, other):
        return Not(Equiv(self, other))

    def __ror__(self, other):
        return Not(Equiv(other, self))

    def __invert__(self):
        return Not(self)

    def __repr__(self):
        return str(self)

class Literal(Formula):
    def __init__(self, lit):
        self.lit = lit

    def __str__(self):
        return str(self.lit)

    def __hash__(self):
        return hash(self.lit)

    def __eq__(self, other):
        return isinstance(other, Literal) and self.lit == other.lit

    def evaluate(self, values):
        return values[self.lit]

    def simplify(self):
        return self

class Not(Formula):
    def __init__(self, term):
        self.term = makeFormula(term)

    def __str__(self):
        return '!(%s)' % self.term

    def __hash__(self):
        return hash(('!', self.term))

    def __eq__(self, other):
        return isinstance(other, Not) and self.term == other.term

    def evaluate(self, values):
        return not self.term.evaluate(values)

    def simplify(self):
        t = self.term.simplify()
        if isinstance(t, Not):
            return t.term
        elif isinstance(t, And):
            return Or([Not(tt) for tt in t.lst]).simplify()
        elif isinstance(t, Or):
            return And([Not(tt) for tt in t.lst]).simplify()
        return Not(t)

class Multi(Formula):
    def __init__(self, *lst):
        if len(lst) == 1:
            lst = lst[0]
        self.lst = frozenset([makeFormula(t) for t in lst])

    def __str__(self):
        if len(self.lst) == 0:
            return self.empty
        else:
            return self.link.join('(%s)' % x for x in self.lst)

    def __hash__(self):
        return hash((self.link, self.lst))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.lst == other.lst

    def evaluate(self, values):
        return self.fun(t.evaluate(values) for t in self.lst)

    def simplify(self):
        s = [t.simplify() for t in self.lst]
        ss = sum([list(t.lst) if isinstance(t, self.__class__) else [t]
                  for t in s], [])
        if len(ss) == 1:
            return ss[0]
        out = self.__class__(ss)
        a = out.absorb()
        if a is None:
            return out
        else:
            return a

    def isEmpty(self):
        return len(self.lst) == 0

class And(Multi):
    empty = 'T'
    link = ' /\ '
    fun = all

    def absorb(self):
        if F in self.lst:
            return F

class Or(Multi):
    empty = 'F'
    link = ' \/ '
    fun = any

    def absorb(self):
        if T in self.lst:
            return T

T = And()
F = Or()

def Tru():
    return T

def Fls():
    return F

def Implies(left, right):
    return Or([Not(left), right])

def Equiv(left, right):
    return And([Implies(left, right), Implies(right, left)])

def makeFormula(term):
    if isinstance(term, Formula):
        return term
    else:
        return Literal(term)
