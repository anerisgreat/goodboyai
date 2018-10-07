from goodboyneuron import neuron, input_neuron

class net(object):
	def __init__(self, n_inputs, n_outputs):
		self.inputs = [input_neuron() for i in range(n_inputs)]
		self.outputs = [neuron(self.inputs) for i in range(n_outputs)]

	def set_input(self, n_input, input_val):
		self.inputs[n_input].set_output(input_val)

	def get_output(self, n_output):
		return output_neurons[i].get_output()
