import numbers


class Expression:
    def __init__(self, *args):
        self.o = args

    def __add__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Add(self, other)
    
    def __radd__(self, other):
        return self + other
        
    def __sub__(self, other):
        if isinstance(self, numbers.Number):
            self = Number(self)
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Sub(self, other)
    
    def __rsub__(self, other):
        return self - other

    def __mul__(self, other):
        if isinstance(self, numbers.Number):
            self = Number(self)
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Mul(self, other)
    
    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Div(self, other)
    
    def __rtruediv__(self, other):
        return self / other

    def __pow__(self, other):
        if isinstance(self, numbers.Number):
            self = Number(self)
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Pow(self, other)


class Terminal(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)

class Operator(Expression):
    def __repr__(self):
        return type(self).__name__ + repr(self.o)
    
    def __str__(self):
        if isinstance(self, Add):
            return f"{str(self.o[0])} + {str(self.o[1])}"
        if isinstance(self, Sub):
            return f"{str(self.o[0])} - {str(self.o[1])}"
        if isinstance(self, Div):
            return f"{str(self.o[0])} / {str(self.o[1])}"
        if isinstance(self, Mul):
            return f"{str(self.o[0])} * {str(self.o[1])}"
        if isinstance(self, Pow):
            return f"{str(self.o[0])} ^ {str(self.o[1])}"

class Number(Terminal):
    def __init__(self, value):
        if isinstance(value, numbers.Number):
            self.value = value


class Symbol(Terminal):
    def __init__(self, value):
        if isinstance(value, str):
            self.value = value

       
class Add(Operator):
    pass

class Sub(Operator):
    pass

class Mul(Operator):
    pass

class Div(Operator):
    pass

class Pow(Operator):
    pass
