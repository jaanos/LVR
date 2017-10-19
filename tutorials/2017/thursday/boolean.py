class Formula:
    def __ne__(self, other):
        return not (self == other)

class Variable(Formula):
    def __init__(self, x):
        self.x = x

    def __str__(self, parentheses = False):
        return str(self.x)

    def __hash__(self):
        return hash(self.x)

    def __eq__(self, other):
        if isinstance(other, Formula):
            return isinstance(other, Variable) and self.x == other.x
        else:
            return self.x == other

    def evaluate(self, values):
        return values[self.x]

    def simplify(self):
        return self

class Not(Formula):
    def __init__(self, x):
        self.x = makeFormula(x)

    def __str__(self, parentheses = False):
        return "~" + self.x.__str__(True)

    def __hash__(self):
        return hash(("~", self.x))

    def __eq__(self, other):
        return isinstance(other, Not) and self.x == other.x

    def evaluate(self, values):
        return not self.x.evaluate(values)

    def simplify(self):
        if isinstance(self.x, Not):
            return self.x.x.simplify()
        elif isinstance(self.x, And):
            return Or(*[Not(y) for y in self.x.terms]).simplify()
        elif isinstance(self.x, Or):
            return And(*[Not(y) for y in self.x.terms]).simplify()
        else:
            return self

class And(Formula):
    def __init__(self, *args):
        self.terms = {makeFormula(x) for x in args}

    def __str__(self, parentheses = False):
        if len(self.terms) == 0:
            return "T"
        elif len(self.terms) == 1:
            return next(iter(self.terms)).__str__(parentheses)
        out = r" /\ ".join(x.__str__(True) for x in self.terms)
        if parentheses:
            return "(%s)" % out
        else:
            return out

    def __hash__(self):
        return hash((r" /\ ", frozenset(self.terms)))

    def __eq__(self, other):
        return isinstance(other, And) and self.terms == other.terms

    def evaluate(self, values):
        return all(x.evaluate(values) for x in self.terms)

    def simplify(self):
        terms = [x.simplify() for x in self.terms]
        if F in terms:
            return F
        terms = [x for x in terms if x != T]
        return And(*terms)

class Or(Formula):
    def __init__(self, *args):
        self.terms = {makeFormula(x) for x in args}

    def __str__(self, parentheses = False):
        if len(self.terms) == 0:
            return "F"
        elif len(self.terms) == 1:
            return next(iter(self.terms)).__str__(parentheses)
        out = r" \/ ".join(x.__str__(True) for x in self.terms)
        if parentheses:
            return "(%s)" % out
        else:
            return out

    def __hash__(self):
        return hash((r" \/ ", frozenset(self.terms)))

    def __eq__(self, other):
        return isinstance(other, Or) and self.terms == other.terms

    def evaluate(self, values):
        return any(x.evaluate(values) for x in self.terms)

    def simplify(self):
        terms = [x.simplify() for x in self.terms]
        if T in terms:
            return T
        terms = [x for x in terms if x != F]
        return Or(*terms)

T = And()
F = Or()

def makeFormula(x):
    if isinstance(x, Formula):
        return x
    else:
        return Variable(x)