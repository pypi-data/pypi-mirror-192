import random
from miniKeras.unit import Variable
# Single neuron
class Neuron:
    
    def __init__(self, inp_size, name=''):
        self.w = [Variable(random.uniform(-1,1), name=name) for i in range(inp_size)]
        self.b = Variable(random.uniform(-1,1))
    

    def __call__(self, x, activation='tanh'):
        if type(x) is not list:
            lis = []
            lis.append(x)
            x = lis.copy()
        res = sum((i*j for i,j in zip(self.w, x)), self.b)
        assert activation in ['relu', 'tanh']
        fin = 'res.'+activation+'()'
        return eval(fin)

    def parameters(self):
        return self.w+[self.b]


class layers:

    class Dense:
        def __init__(self, units, activation='tanh', name=''):
            self.units = units
            self.name = name
            self.activation = activation

        def create_layer(self, inp_size):
            self.neurons = [Neuron(inp_size, name=self.name) for i in range(self.units)]
            
        def __call__(self, x):
            outs = [n(x, self.activation) for n in self.neurons]
            return outs[0] if len(outs)==1 else outs

        def parameters(self):
             return [p for n in self.neurons for p in n.parameters()]

    # More classes to add for different type of layers



class Sequential:
    
    def __init__(self, layers):
        self.layers = layers
    
    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
        
    def parameters(self):
        return [p for l in self.layers for p in l.parameters()]
    
    def Compile(self, alpha=0.01, loss='BinaryCrossEntropy'):
        self.alpha = alpha
        self.loss = loss
        
        
    def fit(self, x, y, running_status=False):
        inp_size = len(x) if type(x) is list else 1
        for l in self.layers:
            l.create_layer(inp_size)
            inp_size = l.units

        loss = Variable(1000)
        iterations = 1000
        i = 0
        while loss.val > 0.001 and i < iterations:
            i += 1
            # forward pass:
            y_pred = [self.__call__(x_) for x_ in x]
            loss = sum((y_out-y_gt)**2 for y_out, y_gt in zip(y_pred, y))
            
            # update:
            for p in self.parameters():
                p.val -= self.alpha*p.grad
            # setting the previous gradients of parameters to zero
            for p in self.parameters():
                p.grad = 0.0
            # backward pass:
            loss.backprop()
            if running_status:
                print("iteration-->",i,"loss=",loss.val)