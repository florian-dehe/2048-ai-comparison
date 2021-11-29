from random import randrange
import math

def sigmoid(x):
    return 1/ (1 + math.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

class Synapse:
    def __init__(self, input, output) -> None:
        self.input = input
        self.output = output
        self.weight = randrange(-1, 1)

class Neuron:
    def __init__(self) -> None:
        self.inputs = [ ]
        self.outputs = [ ]
        self.bias = randrange(-1, 1)

    def __init__(self, input_neurons) -> None:
        self.init()

        for neuron in input_neurons:
            synapse = Synapse(neuron, self)
            neuron.outputs.append(synapse)
            self.inputs.append(synapse)

    def calculate_value(self):
        sum = 0
        for synapse in self.inputs:
            sum += synapse.weight * synapse.input.value + self.bias
        
        self.value = sigmoid(sum)
        return self.value
    
    def calculate_error(self, target):
        return target - self.value
    
    def calculate_gradient(self, target): # output layer
        self.gradient = self.calculate_error(target) * sigmoid_derivative(self.value)
    
    def calculate_gradient(self): # hidden layers
        sum = 0
        for s in self.outputs:
            sum += s.weight * s.input.gradient
        
        self.gradient = sum * sigmoid_derivative(self.value)
    
    def update_weights(self, learning_rate):
        bias_delta = learning_rate * self.gradient
        self.bias += bias_delta

        for s in self.inputs:
            delta = learning_rate * self.gradient * s.input.value
            s.weight += delta
        

class ANN:
    def __init__(self, input_neurons : int, hidden_neuron_per_layers : int, output_neurons : int, num_hidden_layers=1, learn_rate=0.4):
        self.learning_rate = learn_rate
        
        self.input_layer = [ ]
        self.hidden_layers = [ ]
        self.output_layer = [ ]    

        for i in range(input_neurons):
            self.input_layer.append(Neuron())
        
        for i in range(num_hidden_layers):
            self.hidden_layers.append([ ])
            for j in range(hidden_neuron_per_layers):
                self.hidden_layers[i].append(Neuron( self.input_layer if i == 0 else self.hidden_layers[i-1] ))

        for i in output_neurons:
            self.output_layer.append(Neuron(self.hidden_layers[num_hidden_layers-1]))
    
    def train(self, data, num_epochs : int):
        for i in range(num_epochs):
            for set in data:
                self.forward_propagate(set.values)
                self.back_propagate(set.targets)
        
    def train(self, data, minimum_error : float, max_epochs : int):
        error = 1.0
        num_epochs = 0
        while error > minimum_error and num_epochs < max_epochs:
            errors = [ ]
            for set in data:
                self.forward_propagate(set.values)
                self.back_propagate(set.targets)
                errors.append(self.calculate_error(set.targets))
            error /= len(self.output_layer)
            num_epochs += 1
    
    def forward_propagate(self, inputs):
        for i in range(len(inputs)):
            self.input_layer[i].value = inputs[i]
        
        for layer in self.hidden_layers:
            for neuron in layer:
                neuron.calculate_value()
            
        for neuron in self.output_layer:
            neuron.calculate_value()
    
    def back_propagate(self, targets):
        for i in range(len(self.output_layer)):
            self.output_layer[i].calculate_gradient(targets[i])
            self.output_layer[i].update_weights(self.learning_rate)
        
        for i in range(len(self.hidden_layers)-1, -1, -1):
            layer = self.hidden_layers[i]
            for neuron in layer:
                neuron.calculate_gradient()
                neuron.update_weights(self.learning_rate)
    
    def compute(self, inputs):
        self.forward_propagate(inputs)
        result = [ ]
        for neuron in self.output_layer:
            result.append(neuron.value)
        return result
    
    def calculate_error(self, targets):
        sum = 0
        for i in range(len(targets)):
            sum += self.output_layer[i].calculate_error(targets[i])
        return sum

