import numpy as np
from collections import deque
from uuid import uuid4
import math

max_degr_factor = 0.5

class neural_fir(object):
	def __init__(self, taps = [0.25, 0.5, 0.25]):
		self.taps = taps
		self.taps = [1] # override taps for now
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
	return 2 * ((1 / (1 + np.exp(-x))) - 0.01)

class neural_connection(object):
	def __init__(self, in_neuron, weight, degr_factor = max_degr_factor):
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
	def __init__(self, inputs=None, weights = None, bias = 0,\
				degr_factor = 0.001, n_outputs_saved = 100):

		if(not inputs == None):
			if weights == None:
				weights = np.zeros(len(inputs))
			self.connections = [neural_connection(inputs[i], weights[i],\
													degr_factor)
									for i in range(len(inputs))]
		else:
			self.connections = []
		self.bias = bias
		self.fir = neural_fir()
		self.degr_factor = degr_factor
		self.last_iter = -1
		self.output_queue = deque([], n_outputs_saved)
		self.uuid = uuid4()
		self.parents = []
		for i in range(n_outputs_saved):
			self.output_queue.appendleft(0)
		#Initializing endorphinization 
		self.endorphinize_weights = [pow(0.5, i + 1) \
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
		new_connection = neural_connection(other_neuron, weight)
		self.connections.append(new_connection)
		other_neuron.parents.append(self)
	
	def cleanup(self, cleanup_factor = 1e-9):
		connections_to_remove = []
		for connection in self.connections:
			if abs(connection.weight) < cleanup_factor:
				connections_to_remove.append(connection)

		for connection in connections_to_remove:
			self.connections.remove(connection)
			connection.in_neuron.parents.remove(self)
			print('OH NO IM GONE')
	
	def node_deleted(self, node_to_delete):
		to_remove = []
		for connection in self.connections:
			if connection.input_node == node_to_delete:
				to_remove.append(connection)
		for connection in to_remove:
			self.connections.remove(connection)

	def endorphinize(self, value):
		for connection in self.connections:
			contribution = abs(np.inner(self.endorphinize_weights, \
							connection.in_neuron.output_queue))
			connection.degr_factor *= (1 - max(contribution, 0) * value)
			if(abs(connection.degr_factor < 1e-20)):
				if(connection.degr_factor < 0):
					connection.degr_factor = -1e-20
				else:
					connection.degr_factor = 1e-20
			connection.weight *= \
				(1 + contribution * value )

			if(connection.weight > 10000000):
				connection.weight = 10000000
			if(connection.weight < -10000000):
				connection.weight = -10000000

#			if(value > 0):
#				print('OH FUCK YAY SHIT TITS')
#				print('degr factor: ' + str(connection.degr_factor))
#				print('contribution: ' + str(contribution))
#				print('weight: ' + str(connection.weight))

			

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
