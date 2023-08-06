import math
class Variable:

    def __init__(self, val=0, name='', trainable=True, op='', children=()):
        self.val = val
        self.trainable = trainable
        self.grad = 0.0
        self.prev = children
        self.back = lambda : None

        # For better visualization only
        self.op = op
        self.name = name

    def __repr__(self):
        return f"Variable(val = {self.val})"

    def assign(self, val):
        self.val = val
    
    def __add__(self, other):
        other = other if isinstance(other, Variable) else Variable(other)
        output = Variable(self.val+other.val, op='+', children=(self, other))
        def back():
            self.grad += output.grad*1.0
            other.grad += output.grad*1.0
        output.back = back
        return output

    def __mul__(self, other):
        other = other if isinstance(other, Variable) else Variable(other)
        output = Variable(self.val*other.val, op='*', children=(self, other))
        def back():
            self.grad += output.grad*other.val
            other.grad += output.grad*self.val
        output.back = back
        return output

    def __radd__(self, other):
        return self+other
    
    def __rmul__(self, other):
        return  self*other
    
    def __sub__(self, other):
        return self + (-other)
    
    def __truediv__(self, other):
        return self*(other**-1)

    def __pow__(self, other):
        # For simplification only having constant as power
        assert isinstance(other, (int, float))
        output = Variable(self.val**other, op=f'**{other}', children=(self,))
        def back():
            self.grad += output.grad*other*self.val**(other-1)
        output.back = back
        return output
    
    def exp(self):
        output = Variable(math.exp(self.val), op='exp', children=(self,))
        def back():
            self.grad += output.grad*math.exp(self.val)
        output.back = back
        return output

    def tanh(self):
        e = math.exp(2*self.val)
        tan = (e-1)/(e+1)
        output = Variable(tan, op='tanh', children=(self,))
        def back():
            self.grad += output.grad*(1-tan**2)
        output.back = back
        return output

    def backprop(self):
        self.grad = 1.0
        def helper(n):
            n.back()
            for node in n.prev:
                helper(node)
        helper(self)
