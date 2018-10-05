import numpy as np
from collections import deque

class neural_fir(object):
	def __init__(self, taps = [0.25, 0.5, 0.25]):
		self.taps = taps
		self.samps = deque([]) 
		for tap in self.taps:
			self.samps.append(0)
		self.calc_output()

	def calc_output(self):
		output = 0
		for i in range(len(self.taps)):
			output += self.samps[i] * self.taps[i]

		self.output = output
		return self.output

	def insert_sample(self, samp):
		self.samps.append(samp)
		self.samps.popleft()
		self.calc_output()

	def get_output(self):
		return self.output

def sigmoid(x):
	return 1 / (1 + np.exp(-x))

class neuron(object):
	def __init__(self, inputs, weights = None, bias = 0, degr_factor = 0.0001):

		if weights == None:
			weights = np.zeros(len(inputs))

		self.connections = [[inputs[i], weights[i]] for i in range(len(inputs))]
		self.bias = bias
		self.fir = neural_fir()
		self.last_diff = 0
		self.last_output = 0
		self.degr_factor = degr_factor

	def get_output(self):
		sum = 0
		for connection in self.connections:
			weighted_in = connection[0].get_output() * connection[1]
			sum += weighted_in
			connection[1] = connection[1] * (1 - self.degr_factor \
				* abs(connection[0].get_output()))
		sum += self.bias
		self.fir.insert_sample(sigmoid(sum) - 0.5)
		new_output = self.fir.get_output()
		self.last_diff = new_output - self.last_output
		self.last_output = new_output
		return self.last_output

	def get_last_diff(self):
		return self.last_diff

	def connect(self, other_neuron, weight = 0):
		self.connections.append((other_neuron, weight))

class input_neuron(object):
	def __init__(self, output = 0):
		self.output = output

	def set_output(self, n):
		self.output = n

	def get_output(self, ):
		return self.output
