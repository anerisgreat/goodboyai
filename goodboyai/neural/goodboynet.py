from goodboyneuron import neuron, input_neuron
import numpy as np
from numpy.random import choice
import random

class neural_net(object):
	def __init__(self, n_inputs, n_outputs):
		self.inputs = []
		self.outputs = []
		self.outputables = []
		self.inputables = []

		self.current_iter = -1
		for i in range(n_inputs):
			self.add_input()
		for i in range(n_outputs):
			self.add_output()

	def set_input(self, n_input, input_val):
		self.inputs[n_input].set_output(input_val)

	def set_inputs(self, inputs):
		for i in range(len(inputs)):
			self.inputs[i].set_output(inputs[i])

	def add_neuron(self, neu):
		self.outputables.append(neu)
		self.inputables.append(neu)

	def add_input(self):
		new_input = input_neuron()
		self.inputs.append(new_input)
		self.outputables.append(new_input)
	
	def add_output(self):
		new_output = neuron()
		self.outputs.append(new_output)
		self.inputables.append(new_output)

	def get_output(self):
		return [output.get_output(self.current_iter) for output in self.outputs]

	def rand_weight(self, max_weight = 2):
		return (random.random() * 2 * max_weight) - max_weight	
	
	def create_new_rand_neurons(self, n_to_create):
		inputable_choice_weights = [abs(inp.get_output(self.current_iter)) \
					for inp in self.inputables]

		outputable_choice_weights = [abs(outp.get_output(self.current_iter)) \
					for outp in self.outputables]

		to_connect = choice(
				self.inputables,
				n_to_create,
				inputable_choice_weights)

		for neu_to_connect in to_connect:
			new_neu = neuron()
			neu_to_connect.connect(new_neu, self.rand_weight())
			neu_new_inputs = choice(
				self.outputables,
				2, #number of new inputs
				outputable_choice_weights)
			for inp in neu_new_inputs:
				new_neu.connect(inp, self.rand_weight())

			self.add_neuron(new_neu)

	def cleanup(self):
		for outpu in self.outputables:
			outpu.cleanup()

		removed_flag = True
		while removed_flag:
			removed_flag = False
			for outpu in self.outputables:
				if(len(outpu.connections) == 0):
					if(not outpu in self.inputs):
						removed_flag = True
						self.outputables.remove(outpu)
						self.inputables.remove(outpu)
						outpu.node_deleted(self)
						print('BINGO BANGO BONG')
						del(outpu)

	def get_output_and_iterate(self):
		if(self.current_iter % 100 == 0):
			self.cleanup()

		if(self.current_iter % 100 == 0):
			self.create_new_rand_neurons(1)

		if(self.current_iter % 1000 == 0):
			print(self.current_iter)

		self.current_iter += 1 
		ret_output = self.get_output()
	
		return ret_output
	
	def endorphinize(self, n):
		for inputable in self.inputables:
			inputable.endorphinize(n)

