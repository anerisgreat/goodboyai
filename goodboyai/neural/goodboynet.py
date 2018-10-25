from goodboyneuron import neuron, input_neuron
import numpy as np
from numpy.random import choice
import random

class simple_iir(object):
    def __init__(self, factor):
        self.factor = factor
        self.reg = 0
        self.last_output = 0

    def process(self, n):
        ret_val = n - self.reg
        self.reg = self.reg * (1 - self.factor) + n * self.factor
        self.last_output = ret_val
        return ret_val

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

        self.endorph_iir = simple_iir(0.0)
        self.input_iirs = [simple_iir(0.001) for i in range(n_inputs)]
        self.virtual_inputs = [0 for i in range(n_inputs)]

    def set_input(self, n_input, input_val):
        self.virtual_inputs[n_input] = input_val

    def set_inputs(self, inputs):
        for i in range(len(inputs)):
            self.set_input(i, inputs[i])

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
        return [output.get_output(self.current_iter) for output \
                        in self.outputs]

    def rand_weight(self, max_weight = 5):
        return (random.random() * 2 * max_weight) - max_weight  
    
    def create_new_rand_neurons(self, n_to_create):
        inputable_choice_weights = [1 for inp in self.inputables] 

        outputable_choice_weights = \
                        [abs(outp.get_output(self.current_iter)) \
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
        for inpu in self.inputables:
            inpu.cleanup()

        removed_flag = True
        while removed_flag:
            removed_flag = False
            for outpu in self.outputables:
                if(len(outpu.connections) == 0):
                    if(not outpu in self.inputs):
                        removed_flag = True
                        self.remove_node(outpu)

        removed_flag = True
        while removed_flag:
            removed_flag = False
            children = []
            to_remove = []
            for inp in self.inputables:
                for outp in [connection.in_neuron \
                            for connection in inp.connections]:
                    if not outp in self.inputs:
                        if not outp in children:
                            children.append(outp)

            for outp in self.outputables:
                if not outp in children:
                    if not outp in self.inputs:
                        if not outp in to_remove:
                            to_remove.append(outp)

            for removed in to_remove:
                self.remove_node(removed)
                removed_flag = True
    
    def remove_node(self, node_to_remove):
        self.outputables.remove(node_to_remove)
        self.inputables.remove(node_to_remove)
        node_to_remove.node_deleted(self)
        del(node_to_remove)
    
    def get_output_and_iterate(self):
        if(self.current_iter % 10 == 0):
            self.cleanup()

        if(self.current_iter % 1000 == 0):
            if(self.endorph_iir.last_output < 0.8):
                self.create_new_rand_neurons(1)

        self.current_iter += 1 

        #Noisify and put in inputs
        filtered_inputs = [self.input_iirs[i].process(self.virtual_inputs[i])\
                for i in range(len(self.virtual_inputs))]

        noise_factor = 1-max([abs(i) for i in filtered_inputs])\
                /(len(filtered_inputs))

        for i in range(len(filtered_inputs)):
            input_noise = (1 - abs(filtered_inputs[i])) * random.random() \
                    * noise_factor

            self.inputs[i].set_output(input_noise + filtered_inputs[i])

        ret_output = self.get_output()
    
        return ret_output
    
    def endorphinize(self, n):
        endorph_val = self.endorph_iir.process(n)
        #if(n > 0):
        #   print(str(n) + '\t\t' + str(to_endorphinize))
        for inputable in self.inputables:
            inputable.endorphinize(endorph_val)

    def jsonize(self):
        ret = {}
        ret['inputs'] = [inp.jsonize() for inp in self.inputs]
        ret['outputs'] = [outp.jsonize() for outp in self.outputs]
        middles = self.inputables
        for outp in self.outputs:
            middles.remove(outp)

        ret['middles'] = [mid.jsonize() for mid in middles]

        return ret
