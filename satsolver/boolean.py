#!/usr/bin/python

"""
Boolean expressions.
"""

class Formula:
    """
    The superclass for all boolean formulas.

    Provides methods for the operators &, |, ^ and ~ signifying conjunction,
    disjunction, XOR and negation, respectively.
    """

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

    def __rxor__(self, other):
        return Not(Equiv(other, self))

    def __invert__(self):
        return Not(self)

    def __repr__(self):
        return str(self)

class Literal(Formula):
    """
    The class for boolean literals (variables).
    """

    def __init__(self, lit):
        """
        Initialize a literal.

        The input (the name of the literal) may be any hashable object.
        """
        self.lit = lit

    def __str__(self):
        return str(self.lit)

    def __hash__(self):
        return hash(self.lit)

    def __eq__(self, other):
        return isinstance(other, Literal) and self.lit == other.lit

    def evaluate(self, values):
        """
        Evaluate the expression given a dictionary mapping literals to values.

        Returns the value given for the literal. If no value is specified for
        a literal, an error is raised.
        """
        return values[self.lit]

    def simplify(self):
        """
        Simplify the expression.

        A literal is already maximally simplified, so it is returned unchanged.
        """
        return self

class Not(Formula):
    """
    The class for negated expressions.
    """

    def __init__(self, term):
        """
        Initialize a negation.

        The input may be any boolean formula.
        Any other objects will be treated as literals.
        """
        self.term = makeFormula(term)

    def __str__(self):
        return '!(%s)' % self.term

    def __hash__(self):
        return hash(('!', self.term))

    def __eq__(self, other):
        return isinstance(other, Not) and self.term == other.term

    def evaluate(self, values):
        """
        Evaluate the expression given a dictionary mapping literals to values.

        Negates the evaluation of the negated term.
        """
        return not self.term.evaluate(values)

    def simplify(self):
        """
        Simplify the expression.

        Double negations cancel out. Negated conjunctions and disjunctions are
        transformed by De Morgan's laws, thus pushing the negations all the way
        towards literals.
        """
        t = self.term.simplify()
        if isinstance(t, Not):
            return t.term
        elif isinstance(t, And):
            return Or([Not(tt) for tt in t.lst]).simplify()
        elif isinstance(t, Or):
            return And([Not(tt) for tt in t.lst]).simplify()
        return Not(t)

class Multi(Formula):
    """
    A common superclass for conjunctions and disjunctions.
    """

    def __init__(self, *lst):
        """
        Initialize a conjunction or disjunction.

        The input may be a single collection of expressions,
        or any other number of expressions.
        Any other objects will be treated as literals.
        """
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
        """
        Evaluate the expression given a dictionary mapping literals to values.

        Checks that the required number of expressions in the list
        evaluate to True.
        """
        return self.fun(t.evaluate(values) for t in self.lst)

    def simplify(self):
        """
        Simplify the expression.

        Simplifies all subexpressions in the list
        and then flattens any subexpressions of the same type.
        If a single expression remains, that is returned.
        A constant is returned if it absorbs other terms.
        Otherwise, returns a conjuction or disjunction
        of the remaining simplified terms.
        """
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
        """
        Check whether the list is empty, i.e. the expression is constant.
        """
        return len(self.lst) == 0

class And(Multi):
    """
    The class for conjunctions.
    """

    empty = 'T'
    link = ' /\ '
    fun = all

    def absorb(self):
        """
        Return a false constant if it is contained in the list.
        """
        if F in self.lst:
            return F

class Or(Multi):
    """
    The class for disjunctions.
    """

    empty = 'F'
    link = ' \/ '
    fun = any

    def absorb(self):
        """
        Return a true constant if it is contained in the list.
        """
        if T in self.lst:
            return T

T = And()
F = Or()

def Tru():
    """
    Return the true constant.
    """
    return T

def Fls():
    """
    Return the false constant.
    """
    return F

def Implies(left, right):
    """
    Return an implication with the given terms.
    """
    return Or([Not(left), right])

def Equiv(left, right):
    """
    Return an equivalence between the given terms.
    """
    return And([Implies(left, right), Implies(right, left)])

def makeFormula(term):
    """
    Make a formula from an arbitrary object.

    If the input already is a formula, it is returned.
    Otherwise, returns a literal with the given name.
    """
    if isinstance(term, Formula):
        return term
    else:
        return Literal(term)
