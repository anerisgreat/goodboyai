import numpy as np
from collections import deque
from uuid import uuid4
import math
from scipy.signal import firwin

max_degr_factor = 0.05

class neural_fir(object):
    def __init__(self, taps = [0.05, 0.075, 0.125, 0.3, 0.3, \
                                        0.125, 0.075, 0.05, 0.05]):
        self.taps = taps
        self.taps = firwin(7, 0.2) # override taps for now
        self.samps = deque([], len(self.taps)) 
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
    ret = 2 * ((1 / (1 + np.exp(-x)))) - 1
    return ret

class neural_connection(object):
    def __init__(self, in_neuron, weight, degr_factor = max_degr_factor):
        self.in_neuron = in_neuron
        self.weight = weight
        self.degr_factor = degr_factor
    
    def get_output(self, n_iter):
        #Calculate output
        neuron_output = self.in_neuron.get_output(n_iter)
        weighted_in = self.weight * neuron_output
        #Degrade weight
        #self.weight *= (1 - self.degr_factor * abs(neuron_output))
        change = self.degr_factor * abs(neuron_output)
        if(self.weight > change):
            self.weight -= change
        elif(self.weight < -change):
            self.weight += change
        else:
            self.weight = 0

        return weighted_in

    def jsonize(self):
        ret = {}
        ret['weight'] = self.weight
        ret['degr_factor'] = self.degr_factor
        ret['node_uuid'] = str(self.in_neuron.uuid)

        return ret

class neuron(object):
    def __init__(self, inputs=None, weights = None, bias = 0,\
                degr_factor = max_degr_factor, n_outputs_saved = 100):

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
    
    def cleanup(self, cleanup_factor = 1):
        connections_to_remove = []
        for connection in self.connections:
            if (abs(connection.weight) <= cleanup_factor or \
                ((not type(connection.in_neuron) is input_neuron) and \
                    (len(connection.in_neuron.connections) == 0)) ):
                connections_to_remove.append(connection)

        for connection in connections_to_remove:
            self.connections.remove(connection)
    
    def node_deleted(self, node_to_delete):
        to_remove = []
        for connection in self.connections:
            if connection.in_neuron == node_to_delete:
                to_remove.append(connection)
        for connection in to_remove:
            self.connections.remove(connection)

    def endorphinize(self, value):
        if(value == 0):
            return
        for connection in self.connections:
            weight_sign = 1
            if(connection.weight < 0):
                weight_sign = -1

            contribution = abs((np.inner(self.endorphinize_weights, \
                            connection.in_neuron.output_queue)))

            #connection.degr_factor *= (1 - max(contribution, 0) * value)
            change = contribution * value * weight_sign * 0.5
            if(value < -300):
                print(change)
                print('AND NOW')
           # if(False and value > 0.01):
                #print('Welcome to the endorphinization station')
                #print('UUID: ' + str(self.uuid))
                #print('VALUE: ' + str(value))
                #print('CONN UUID: ' + str(connection.in_neuron.uuid))
                #print('CHANGE: ' + str(change))
            if(change * connection.weight < 0 \
                and abs(connection.weight) < abs(change)):
                connection.weight = 0
            else:
                #if(value < 0):
                    #print(connection.weight)
                    #print('AND NOW')
                connection.weight += change
                #if(value < 0):
                    #print(connection.weight)
                    #print('DONE NOW')

    def jsonize(self):
        ret = {}
        ret['uuid'] = str(self.uuid)
        ret['connections'] = [connection.jsonize() for connection\
                    in self.connections]

        return ret

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

    def jsonize(self):
        ret = {}
        ret['uuid'] = str(self.uuid)
        return ret
