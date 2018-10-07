from goodboyneuron import neuron, input_neuron


def print_outputs(neu, n):
	for i in range(n):
		print(neu.get_output(i))

def main():
	inp1 = input_neuron(1)
	inp2 = input_neuron(0)
	inp3 = input_neuron(0)

	out1 = neuron(inputs = [inp1, inp2, inp3], weights = [1, 1, 1], bias = 0)

	print('PHASE 1.1')
	print_outputs(out1, 10)

	inp1.set_output(0)
	inp2.set_output(1)
	
	print('PHASE 1.2')
	print_outputs(out1, 10)

	out1.endorphinize(1)

	inp2.set_output(0)
	inp3.set_output(1)

	print('PHASE 1.3')
	print_outputs(out1, 10)

	print('END PHASE 1, PHASE 2')
	inp1.set_output(1)
	inp2.set_output(0)
	inp3.set_output(0)
	print('PHASE 2.1')
	print_outputs(out1, 3)

	inp1.set_output(0)
	inp2.set_output(1)
	inp3.set_output(0)

	print('PHASE 2.2')
	print_outputs(out1, 3)
	inp1.set_output(0)
	inp2.set_output(0)
	inp3.set_output(1)

	print('PHASE 2.3')
	print_outputs(out1, 3)

if __name__ == "__main__":
	main()
