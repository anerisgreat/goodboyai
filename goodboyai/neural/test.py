from neuron import neuron, input_neuron

def main():
	inp1 = input_neuron()
	inp1.set_output(2)

	inp2 = input_neuron(1)

	out1 = neuron(inputs = [inp1, inp2], weights = [1, 1], bias = 0)

	print(out1.get_output())

if __name__ == "__main__":
	main()