from __future__ import print_function
import time

class test_sim_world(object):
	def __init__(self, size = 49):
		self.creature_pos = 0
		self.size = size

	def iter_and_ret_str(self):
		ret_str = list([' ' for i in range(self.size)])
		ret_str[len(ret_str) / 2 + self.creature_pos]='X'
		self.creature_pos += 1
		if(self.creature_pos > self.size / 2):
			self.creature_pos = -self.size/2 + 1
		return ''.join(ret_str)
def main():
	t = test_sim_world()
	for i in range(1000):
		print(t.iter_and_ret_str(), end = '\r')
		time.sleep(0.01)
if __name__ == '__main__':
	main()
