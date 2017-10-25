class Formula:
    def __ne__(self, other):
        return not (self == other)

    def flatten(self):
        return self

    def getVariable(self, mapping):
        if self not in mapping:
            mapping[self] = freshVariable()
        return mapping[self]

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

    def tseytin(self, mapping):
        return self

    def equiv(self, variable):
        return And(Or(variable, Not(self)), Or(Not(variable), self))

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

    def flatten(self):
        if isinstance(self.x, Not):
            return self.x.x
        else:
            return self

    def simplify(self):
        if isinstance(self.x, And):
            return Or(*(Not(y) for y in self.x.terms)).simplify()
        elif isinstance(self.x, Or):
            return And(*(Not(y) for y in self.x.terms)).simplify()
        else:
            return self.flatten().simplify()

    def tseytin(self, mapping):
        return Not(self.x.tseytin(mapping)).getVariable(mapping)

    def equiv(self, variable):
        return And(Or(variable, self.x), Or(Not(variable), self))

class Multi(Formula):
    def __init__(self, *args):
        self.terms = frozenset(makeFormula(x) for x in args)

    def __str__(self, parentheses = False):
        if len(self.terms) == 0:
            return self.empty
        elif len(self.terms) == 1:
            return next(iter(self.terms)).__str__(parentheses)
        out = self.connective.join(x.__str__(True) for x in self.terms)
        if parentheses:
            return "(%s)" % out
        else:
            return out

    def __hash__(self):
        return hash((self.connective, self.terms))

    def __eq__(self, other):
        return isinstance(other, self.getClass()) \
            and self.terms == other.terms

    def evaluate(self, values):
        return self.fun(x.evaluate(values) for x in self.terms)

    def flatten(self):
        this = self.getClass()
        terms = (x.flatten() for x in self.terms)
        out = this(*sum([list(x.terms) if isinstance(x, this)
                         else [x] for x in terms], []))
        if len(out.terms) == 1:
            return next(iter(out.terms))
        else:
            return out

    def simplify(self):
        terms = [x.simplify() for x in self.terms]
        const = self.getDualClass()()
        if const in terms:
            return const
        if len(terms) == 1:
            return terms[0]
        return self.getClass()(*terms).flatten()

    def tseytin(self, mapping):
        return self.getClass()(*(x.tseytin(mapping)
                               for x in self.terms)).getVariable(mapping)

class And(Multi):
    empty = "T"
    connective = r" /\ "
    fun = all

    def getClass(self):
        return And

    def getDualClass(self):
        return Or

    def equiv(self, variable):
        return And(Or(variable, *(Not(x).flatten() for x in self.terms)),
                   *(Or(Not(variable), x) for x in self.terms))

class Or(Multi):
    empty = "F"
    connective = r" \/ "
    fun = any

    def getClass(self):
        return Or

    def getDualClass(self):
        return And

    def equiv(self, variable):
        return And(Or(Not(variable), *self.terms),
                   *(Or(variable, Not(x)) for x in self.terms))

T = And()
F = Or()

def makeFormula(x):
    if isinstance(x, Formula):
        return x
    else:
        return Variable(x)

counter = 0

def freshVariable():
    global counter
    counter += 1
    return Variable(("__", counter))

def tseytin(formula, mapping = None):
    if mapping is None:
        mapping = {}
    f = formula.tseytin(mapping)
    return And(f, *(k.equiv(v) for k, v in mapping.items())).flatten()
