class Formula:
    def __ne__(self, other):
        return not (self == other)

class Variable(Formula):
    def __init__(self, x):
        self.x = x

    def __str__(self, parenthesise = False):
        return str(self.x)

    def __eq__(self, other):
        if isinstance(other, Formula):
            return isinstance(other, Variable) and self.x == other.x
        else:
            return self.x == other

    def __hash__(self):
        return hash(self.x)

    def evaluate(self, values):
        return values[self.x]

    def simplify(self):
        return self

class Not(Formula):
    def __init__(self, x):
        self.x = makeFormula(x)

    def __str__(self, parenthesise = False):
        return "!" + self.x.__str__(True)

    def __eq__(self, other):
        return isinstance(other, Not) and self.x == other.x

    def evaluate(self, values):
        return not self.x.evaluate(values)

    def simplify(self):
        if isinstance(self.x, Not):
            return self.x.x.simplify()
        elif isinstance(self.x, And):
            return Or(*[Not(x).simplify() for x in self.x.terms])
        elif isinstance(self.x, Or):
            return And(*[Not(x).simplify() for x in self.x.terms])
        else:
            return self

class And(Formula):
    def __init__(self, *args):
        self.terms = [makeFormula(x) for x in args]

    def __str__(self, parenthesise = False):
        if len(self.terms) == 0:
            return 'T'
        elif len(self.terms) == 1:
            return self.terms[0].__str__(parenthesise)
        out = " & ".join(x.__str__(True) for x in self.terms)
        if parenthesise:
            return "(" + out + ")"
        else:
            return out

    def __eq__(self, other):
        return isinstance(other, And) and \
            len(self.terms) == len(other.terms) and \
            all(x == y for x, y in zip(self.terms, other.terms))

    def evaluate(self, values):
        return all(x.evaluate(values) for x in self.terms)

    def simplify(self):
        self.terms = [x.simplify() for x in self.terms]
        if F in self.terms:
            return F
        self.terms = [x for x in self.terms if x != T]
        if len(self.terms) == 1:
            return self.terms[0]
        else:
            return self

class Or(Formula):
    def __init__(self, *args):
        self.terms = [makeFormula(x) for x in args]

    def __str__(self, parenthesise = False):
        if len(self.terms) == 0:
            return 'F'
        elif len(self.terms) == 1:
            return self.terms[0].__str__(parenthesise)
        out = " | ".join(x.__str__(True) for x in self.terms)
        if parenthesise:
            return "(" + out + ")"
        else:
            return out

    def __eq__(self, other):
        return isinstance(other, Or) and \
            len(self.terms) == len(other.terms) and \
            all(x == y for x, y in zip(self.terms, other.terms))

    def evaluate(self, values):
        return any(x.evaluate(values) for x in self.terms)

    def simplify(self):
        self.terms = [x.simplify() for x in self.terms]
        if T in self.terms:
            return T
        self.terms = [x for x in self.terms if x != F]
        if len(self.terms) == 1:
            return self.terms[0]
        else:
            return self

T = And()
F = Or()

def makeFormula(x):
    if isinstance(x, Formula):
        return x
    else:
        return Variable(x)
