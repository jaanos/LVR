class Formula:
    pass

class Variable(Formula):
    def __init__(self, x):
        self.x = x

    def __str__(self, parentheses = False):
        return str(self.x)

class Not(Formula):
    def __init__(self, x):
        self.x = makeFormula(x)

    def __str__(self, parentheses = False):
        return "~" + self.x.__str__(True)

class And(Formula):
    def __init__(self, *args):
        self.terms = [makeFormula(x) for x in args]

    def __str__(self, parentheses = False):
        if len(self.terms) == 0:
            return "T"
        elif len(self.terms) == 1:
            return self.terms[0].__str__(parentheses)
        out = r" /\ ".join(x.__str__(True) for x in self.terms)
        if parentheses:
            return "(%s)" % out
        else:
            return out

class Or(Formula):
    def __init__(self, *args):
        self.terms = [makeFormula(x) for x in args]

    def __str__(self, parentheses = False):
        if len(self.terms) == 0:
            return "F"
        elif len(self.terms) == 1:
            return self.terms[0].__str__(parentheses)
        out = r" \/ ".join(x.__str__(True) for x in self.terms)
        if parentheses:
            return "(%s)" % out
        else:
            return out

def makeFormula(x):
    if isinstance(x, Formula):
        return x
    else:
        return Variable(x)