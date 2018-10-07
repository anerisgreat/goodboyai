import numpy as np
from numpy import inner
from goodboyneuron import neuron, input_neuron
from goodboynet import neural_net
import random


def print_outputs(neu, n):
	for i in range(n):
		print(neu.get_output(i))

def test_single_neurons():
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

	print('DEGR_FACTORS:')
	print([c.degr_factor for c in out1.connections])
	print([c.weight for c in out1.connections])


def main():
	#test_single_neurons()
	leng = 3
	net = neural_net(leng, leng)	
	wf = open('log.csv', 'w')
	#while True:
	for p in range(100000):
		iter_input = []
		input_num = random.randrange(leng)
		for i in range(leng):
			if(i == input_num):
				random_select = random.randrange(2)
				if(random_select)==1:
					iter_input.append(1)
				else:
					iter_input.append(-1)
			else:
				iter_input.append(0)
		for x in range(1000):
			net.set_inputs(iter_input)
			iter_output = net.get_output_and_iterate()

			endorphinize = inner(iter_input, iter_output) * 1

			#endorphinize = iter_input[0] * iter_output[0]
			#for j in range(1, leng):
			#	endorphinize = min(endorphinize, iter_input[j] * iter_output[j])
			endorphinize *= 1
			#print(endorphinize)

			net.endorphinize(endorphinize)
			#print('ITER')
			#print('INPUT: ' + str(iter_input))
			#print('OUTPUT: ' + str(iter_output))
			#print('ENDORPHINIZE: ' + str(endorphinize))

			wf.write(str(endorphinize) + ',')
#			if(raw_input() == 'q'):
#				wf.close()
#				exit()

	wf.close()
	exit()

		
if __name__ == "__main__":
	main()
