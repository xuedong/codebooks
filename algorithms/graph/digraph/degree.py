"""
Degree distributions for graphs
"""

EX_GRAPH0 = {0: set([1, 2]),
			 1: set([]),
			 2: set([])}

EX_GRAPH1 = {0: set([1, 4, 5]),
			 1: set([2, 6]),
			 2: set([3]),
			 3: set([0]),
			 4: set([1]),
			 5: set([2]),
			 6: set([])}

EX_GRAPH2 = {0: set([1, 4, 5]),
			 1: set([2, 6]),
			 2: set([3, 7]),
			 3: set([7]),
			 4: set([1]),
			 5: set([2]),
			 6: set([]),
			 7: set([3]),
			 8: set([1, 2]),
			 9: set([0, 3, 4, 5, 6, 7])}

# This is a module that
# computes a directed graph's
# in-degree distribution

def make_complete_graph(num_nodes):
	"""
	Generate a complete directed graph as a dictionary
	"""
	graph = {}
	nodes = range(num_nodes)
	for node in nodes:
		graph[node] = set(range(num_nodes))
		(graph[node]).remove(node)
	return graph

def compute_in_degrees(digraph):
	"""
	Compute the in-degrees for the nodes in digraph
	and store them in a dictionary
	"""
	in_degrees = {}
	for key_i in digraph:
		degree = 0
		for key_j in digraph:
			if key_i in digraph[key_j]:
				degree += 1
		in_degrees[key_i] = degree
	return in_degrees

def in_degree_distribution(digraph):
	"""
	Compute the in-degree distribution of digraph
	"""
	dist = {}
	in_degrees = compute_in_degrees(digraph)
	for key in in_degrees:
		if dist.has_key(in_degrees[key]):
			dist[in_degrees[key]] += 1
		else:
			dist[in_degrees[key]] = 1
	return dist