from __future__ import print_function
import time
import random
from goodboynet import neural_net
import curses
import json

class test_sim_world(object):
    def __init__(self, term_width = 50):
        self.world_size = 50
        self.creature_pos = float(self.world_size / 2)
        self.term_width = term_width
        self.is_there_food = True
        self.food_pos = random.random() * self.world_size * 0.4 + 0.3
        self.net = neural_net(4, 1)
        self.log_file = open('food_log.log', 'w')
    def iter_and_ret_str(self):
        #Move based on previous outputs

        ENDORPH_NUM = 10000

        iter_output = self.net.get_output_and_iterate()
        endorphinize = 0

        #Position and endorphinization
        self.creature_pos += iter_output[0] * 1
        hit = False
        if(self.creature_pos < 0):
            hit = True
            self.creature_pos = 0
        elif(self.creature_pos > self.world_size):
            hit = True
            self.creature_pos = self.world_size

        if(hit):
            endorphinize -= ENDORPH_NUM

        if (self.is_there_food and \
                abs(self.creature_pos - self.food_pos) < 1):
            endorphinize += ENDORPH_NUM * 2
            self.food_pos = random.random() * self.world_size


        self.net.endorphinize(endorphinize)

        left_wall_neuron = max((1 - self.creature_pos / 10), 0)
        right_wall_neuron = max((1 - \
                abs(self.world_size - self.creature_pos) / 10), 0)

        food_neur_val = max((1 - \
                abs(self.food_pos - self.creature_pos) / self.world_size), 0)

        left_food_neuron = 0
        right_food_neuron = 0

        if(self.food_pos < self.creature_pos):
            #left_food_neuron = food_neur_val
            left_food_neuron = 1
        else:
            #right_food_neuron = food_neur_val
            right_food_neuron = 1

        iter_inputs = [left_food_neuron, right_food_neuron, left_wall_neuron, right_wall_neuron]
                

        self.net.set_inputs(iter_inputs)	

        ret_str = list([' ' for i in range(self.term_width)])
        diff = self.world_size / self.term_width
        for i in range(self.term_width):
            if(abs(self.food_pos - (i * diff)) < (diff)):
                ret_str[i] = 'F'

            if(abs(self.creature_pos - (i * diff)) < diff):
                ret_str[i] = 'X'


        self.log_file.write(str(len(self.net.outputables)) + 
                '    ' + str(endorphinize) + 
                '    ' + '{:10.1f}'.format(iter_output[0]) +
                '    ' + '{:10.1f}'.format(self.creature_pos) +
                '    ' + str(iter_inputs) + '\r\n')
        return '|' + ''.join(ret_str) + '|'

def main():
    term_width = 50
    t = test_sim_world(term_width = term_width - 2)

    for i in range(100000):
        print(t.iter_and_ret_str(), end = '\r')

    wf2 = open('food_net_json.json', 'w')
    wf2.write(json.dumps(t.net.jsonize(), indent = 4))
    wf2.close()
if __name__ == '__main__':
     main()
