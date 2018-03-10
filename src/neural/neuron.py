import numpy as np

def sigmoid(x):
	return 1 / (1 + np.exp(-x))

class neuron(object):
	def __init__(self, inputs, weights = None, bias = 0):

		if weights == None:
			weights = np.zeros(len(inputs))

		self.connections = [(inputs[i], weights[i]) for i in range(len(inputs))]
		self.bias = bias
		self.last_output = 0

	

	def get_output(self):
		sum = 0
		for connection in self.connections:
			sum += connection[0].get_output() * connection[1]
		sum += self.bias
		self.last_output = sigmoid(sum)
		return self.last_output


class input_neuron(object):
	def __init__(self, output = 0):
		self.output = output

	def set_output(self, n):
		self.output = n

	def get_output(self, ):
		return self.output