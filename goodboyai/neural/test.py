import numpy as np
from numpy import inner
from goodboyneuron import neuron, input_neuron
from goodboynet import neural_net
import random
import json

def print_outputs(neu, n):
	for i in range(n):
		print(neu.get_output(i))

def test_single_neurons():
	inp1 = input_neuron(1)
	inp2 = input_neuron(0)
	inp3 = input_neuron(0)

	out1 = neuron(inputs = [inp1, inp2, inp3], \
				weights = [1, 1, 1], bias = 0)

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
	for p in range(500):
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

				#iter_input.append(0)
		for x in range(100):
			net.set_inputs(iter_input)
			iter_output = net.get_output_and_iterate()

			endorphinize = inner(iter_input, iter_output) / 3

			endorphinize *= 1000
			#print(endorphinize)

			#if(not endorphinize == 0):
			if(False):
			#print('ITER')
				print('INPUT: ' + str(iter_input))
				print('OUTPUT: ' + str(iter_output))
				print('ENDORPHINIZE: ' + str(endorphinize))
				print('FUCKING OUTPUTABLES: ' + str(len(net.outputables)))
				print('WEIGHTS: ')
				print('Inputs: ')
				for inp in net.inputs:
					print('UUID: ' + str(inp.uuid))
				for inputable in net.inputables:
					print('INPUTABLE')
					print('    UUID ' + str(inputable.uuid))
					print('    IS OUTPUT: ' + str(inputable in net.outputs))
					for connection in inputable.connections:
						print('        WEIGHT: ' + str(connection.weight))
						print('        UID: ' + str(connection.in_neuron.uuid))
				if(raw_input() == 'q'):
					wf.close()
					exit()
			net.endorphinize(endorphinize)

			wf.write(str(endorphinize) + ',' + str(len(net.inputables)) + ',' + str(iter_input) + ',' + str(iter_output) + '\r\n')
		for x in range(10):
			net.set_inputs([0 for i in range(leng)])
			iter_output = net.get_output_and_iterate()


	
	wf.close()
	wf2 = open('net_json.json', 'w')
	wf2.write(json.dumps(net.jsonize(), indent = 4))
	wf2.close()
		
if __name__ == "__main__":
	main()
