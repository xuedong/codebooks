"""
Graph resilience
"""

import random
from collections import deque

def bfs_visited(ugraph, start_node):
	"""
	Breadth-first search visited algorithm
	"""
	queue = deque()
	visited = set([start_node])
	queue.append(start_node)

	while queue:
		node = queue.pop()
		neighbors = ugraph[node]
		for neighbor in neighbors:
			if neighbor not in visited:
				visited.add(neighbor)
				queue.append(neighbor)

	return visited

def cc_visited(ugraph):
	"""
	Compute the connected components
	of the given undirected graph
	"""
	remaining = ugraph.keys()
	ccs = []

	while remaining:
		node = random.choice(remaining)
		component = bfs_visited(ugraph, node)
		if not(component in ccs):
			ccs.append(component)
		remaining.remove(node)

	return ccs

def largest_cc_size(ugraph):
	"""
	Return the size of the largest connected
	component in ugraph
	"""
	ccs = cc_visited(ugraph)
	sizes = [len(component) for component in ccs]
	if sizes == []:
		return 0
	else:
		return max(sizes)

def compute_resilience(ugraph, attack_order):
	"""
	Compute the resilience of a computer network
	"""
	resiliences = [largest_cc_size(ugraph)]
	graph = ugraph

	for node in attack_order:
		neighbors = graph.pop(node, None)
		for neighbor in neighbors:
			if node in graph[neighbor]:
				graph[neighbor].remove(node)
		resiliences.append(largest_cc_size(graph))

	return resiliences