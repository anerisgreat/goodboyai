import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
def main(args):
	fr = open(args[0], 'r')
	data_str = json.loads(fr.read())

	gr = nx.MultiDiGraph()

	mid_uuid = [middle['uuid'] for middle in data_str['middles']]
	gr.add_nodes_from(mid_uuid)
	outp_uuid = [outp['uuid'] for outp in data_str['outputs']]
	gr.add_nodes_from(outp_uuid)
	inp_uuid = [inp['uuid'] for inp in data_str['inputs']]
	gr.add_nodes_from(inp_uuid)
	
	connections = []
	connect_label_dict = {}
	for middle in data_str['middles']:
		for connect in middle['connections']:
			tup = (connect['node_uuid'], middle['uuid'])
			connect_label_dict[tup] = '{:10.1f}'.format(connect['weight'])
			connections.append((tup, {'weight' : str(connect['weight'])}))


	for outp in data_str['outputs']:
		for connect in outp['connections']:
			tup = (connect['node_uuid'], outp['uuid'])
			connect_label_dict[tup] = '{:10.1f}'.format(connect['weight'])
			#connections.append(tup)
			connections.append((tup, {'weight' : float(connect['weight'])}))

	for conn in connections:
		gr.add_edge(conn[0][0], conn[0][1], attr_dict = None, weight = abs(float(conn[1]['weight'])))

	color_map = []
	for node in gr:
		if node in mid_uuid:
			color_map.append('blue')
		elif node in outp_uuid:
			color_map.append('green')
		else:
			color_map.append('red')

	#pos = nx.circular_layout(gr)
	pos = nx.spring_layout(gr)

	nx.draw(gr, node_color = color_map, pos = pos, with_labels = False)
	nx.draw_networkx_edge_labels(gr, pos = pos, \
			edge_labels = connect_label_dict) 
	plt.show()

	print(connect_label_dict) 

if(__name__ == '__main__'):
	main(sys.argv[1:])
