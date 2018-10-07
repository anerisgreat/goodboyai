import numpy as np
from collections import deque

class neural_fir(object):
	def __init__(self, taps = [0.25, 0.5, 0.25]):
		self.taps = taps
		self.samps = deque([], len(taps)) 
		for i in range(len(self.taps) + 1):
			self.samps.appendleft(float(0))
		self.calc_output()

	def calc_output(self):
		output = 0
		for i in range(len(self.taps)):
			output += self.samps[i] * self.taps[i]

		self.output = output
		return self.output

	def insert_sample(self, samp):
		self.samps.appendleft(samp)
		self.calc_output()

	def get_output(self):
		return self.output

def sigmoid(x):
	return 2 * ((1 / (1 + np.exp(-x))) - 0.5)

class neural_connection(object):
	def __init__(self, in_neuron, weight, degr_factor):
		self.in_neuron = in_neuron
		self.weight = weight
		self.degr_factor = degr_factor
	
	def get_output(self, n_iter):
		#Calculate output
		neuron_output = self.in_neuron.get_output(n_iter)
		weighted_in = neuron_output * self.weight
		#Degrade weight
		self.weight *= (1 - self.degr_factor * abs(neuron_output))
		return weighted_in

class neuron(object):
	def __init__(self, inputs, weights = None, bias = 0, degr_factor = 0.001,\
				n_outputs_saved = 100):

		if weights == None:
			weights = np.zeros(len(inputs))

		self.connections = [neural_connection(inputs[i], weights[i],\
												degr_factor)
								for i in range(len(inputs))]
		self.bias = bias
		self.fir = neural_fir()
		self.degr_factor = degr_factor
		self.last_iter = -1
		self.output_queue = deque([], n_outputs_saved)
		for i in range(n_outputs_saved):
			self.output_queue.appendleft(0)
		#Initializing endorphinization 
		self.endorphinize_weights = [pow(0.5, i - 1) \
										for i in range(n_outputs_saved)] 

	def get_output(self, n_iter):
		if(n_iter == self.last_iter):
			return self.last_output()
		self.last_iter = n_iter
		sum = 0
		for connection in self.connections:
			sum += connection.get_output(n_iter)
		sum += self.bias
		self.fir.insert_sample(sigmoid(sum))
		new_output = self.fir.get_output()
		self.output_queue.appendleft(self.fir.get_output())

		return self.last_output()

	def last_output(self):
		return self.output_queue[0]
	
	def connect(self, other_neuron, weight = 0):
		self.connections.appendleft((other_neuron, weight))

	def endorphinize(self, value):
		for connection in self.connections:
			contribution = np.inner(self.endorphinize_weights, \
							connection.in_neuron.output_queue)
			connection.weight *= (1 + contribution)
			connection.degr_factor /= (1 + contribution)

class input_neuron(neuron):
	def __init__(self, output = 0):
		neuron.__init__(self, [])
		self.output = output

	def set_output(self, n):
		self.output = n

	def get_output(self, n_iter):
		if(n_iter == self.last_iter):
			return self.last_output()

		self.output_queue.appendleft(self.output)
		return self.last_output()
