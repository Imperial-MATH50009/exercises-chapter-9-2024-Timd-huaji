import numbers  # noqa D100
from functools import wraps
from functools import singledispatch


def postvisitor(exp, fn, **kwargs):
    """DAG Postvisitor method that evaluate each expression only once."""
    stack = [exp]
    visited = {}

    while stack:
        e = stack.pop()
        unvisited_children = []

        for o in e.operands:
            if o not in visited:
                unvisited_children.append(o)
        if unvisited_children:
            stack.append(e)
            stack += unvisited_children
        else:
            visited[e] = fn(e, *(visited[o] for o in e.operands),
                            **kwargs)

    return visited[exp]


def inst_number(meth):
    """Define a general single dispatching function."""
    """Turns a numbers.Number second operand into a Number operand"""
    """and return the expression."""

    @wraps(meth)
    def fn(self, other):
        if isinstance(other, Expression) or isinstance(other, Symbol):
            return meth(self, other)
        elif isinstance(other, numbers.Number):
            other = Number(other)
            return meth(self, other)
        else:
            return NotImplemented
    return fn


class Expression:
    """The expression class that defines basic operations."""

    def __init__(self, *args):
        """Instantiate the expression object."""
        self.operands = args

    @inst_number
    def __add__(self, other):
        """Override the add magic method, return an Add expression."""
        return Add(self, other)

    @inst_number
    def __radd__(self, other):
        """Override the radd magic method, return a Add expression."""
        return Add(other, self)

    @inst_number
    def __sub__(self, other):
        """Override the sub magic method, return an Sub expression."""
        return Sub(self, other)

    @inst_number
    def __rsub__(self, other):
        """Override the rsub magic method, return a Sub expression."""
        return Sub(other, self)

    @inst_number
    def __mul__(self, other):
        """Override the mul magic method, return a Mul expression."""
        return Mul(self, other)

    @inst_number
    def __rmul__(self, other):
        """Override the rmul magic method, return a Mul expression."""
        return Mul(other, self)

    @inst_number
    def __truediv__(self, other):
        """Override the truediv magic method, return a Div expression."""
        return Div(self, other)

    @inst_number
    def __rtruediv__(self, other):
        """Override the rtruediv magic method, return a Div expression."""
        return Div(other, self)

    @inst_number
    def __pow__(self, other):
        """Override the pow magic method, return a Pow expression."""
        return Pow(self, other)

    @inst_number
    def __rpow__(self, other):
        """Override the rpow magic method, return a Pow expression."""
        return Pow(other, self)


class Terminal(Expression):
    """The basic class for terminals, define basic properties."""

    def __init__(self, value):
        """Instantiate the terminal with an empty operand but a value."""
        self.operands = ()
        self.value = value

    def __repr__(self):
        """Return the repr of the terminal."""
        return repr(self.value)

    def __str__(self):
        """Return the string representation of the terminal."""
        return str(self.value)


class Operator(Expression):
    """The Operator class that defines common properties for operators."""

    def __repr__(self):
        """Return the repr of the expression, specific to actual operator."""
        return type(self).__name__ + repr(self.operands)

    def __str__(self):
        """Return the repr of the expression, specific to actual operator."""
        operator = {"Add": "+", "Sub": "-", "Mul": "*", "Div": "/", "Pow": "^"}
        operand1, operand2 = str(self.operands[0]), str(self.operands[1])
        if self.order > self.operands[0].order:
            operand1 = "(" + operand1 + ")"
        if self.order > self.operands[1].order:
            operand2 = "(" + operand2 + ")"
        return f"{operand1} {operator[type(self).__name__]} {operand2}"


class Number(Terminal):
    """The Number subclass of terminal, help instantiating numbers."""

    order = float('inf')

    def __init__(self, value):
        """Instantiate a Number object with no operands but a value."""
        if isinstance(value, numbers.Number):
            self.operands = ()
            self.value = value


class Symbol(Terminal):
    """The Symbol subclass of terminal, help instantiating symbols."""

    order = float('inf')

    def __init__(self, value):
        """Instantiate a Symbol object with no operands but a (str) value."""
        if isinstance(value, str):
            self.operands = ()
            self.value = value


class Add(Operator):
    """Define the add subclass with operation precedence 1."""

    order = 1
    pass


class Sub(Operator):
    """Define the subtraction subclass with operation precedence 1."""

    order = 1
    pass


class Mul(Operator):
    """Define the multiplication subclass with operation precedence 2."""

    order = 2
    pass


class Div(Operator):
    """Define the (true) division subclass with operation precedence 2."""

    order = 2
    pass


class Pow(Operator):
    """Define the power operation subclass with operation precedence 3."""

    order = 3
    pass


@singledispatch
def differentiate(expr, *o, **kwargs):
    """Single dispatch differentiate function."""
    raise NotImplementedError(
        f"Cannot differentiate a {type(expr).__name__}")


@differentiate.register(Number)
def _(expr, *o, **kwargs):
    return 0


@differentiate.register(Symbol)
def _(expr, *o, var, **kwargs):
    return Number(1) if expr.value == var else Number(0)


@differentiate.register(Add)
def _(expr, *o, **kwargs):
    return o[0] + o[1]


@differentiate.register(Sub)
def _(expr, *o, **kwargs):
    return o[0] - o[1]


@differentiate.register(Mul)
def _(expr, *o, **kwargs):
    return o[0] * expr.operands[1] + o[1] * expr.operands[0]


@differentiate.register(Div)
def _(expr, *o, **kwargs):
    return (expr.operands[1] * o[0] - expr.operands[0] * o[1]) \
            / expr.operands[1] ** 2


@differentiate.register(Pow)
def _(expr, *o, **kwargs):
    return o[0] * expr.operands[1] * expr.operands[0] ** (expr.operands[1] - 1)
