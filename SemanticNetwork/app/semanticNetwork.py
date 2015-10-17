from abc import abstractmethod
import networkx as nx
import matplotlib.pyplot as plt
import logging

__author__ = 'federico'

logger = logging.getLogger("Fallas2")

class SemanticNetwork:
	def __init__(self):
		self.graph = nx.Graph()
		self.labels = {}

	def add_object(self, objectStr):
		self.graph.add_node(objectStr)

	# Call example: add_node_from(['One'. 'Two'])
	def add_object_from(self, objectsStr):
		self.graph.add_node_from(objectsStr)

	def add_relation(self, objectA, objectB, relationName):
		self.graph.add_edge(objectA, objectB)
		self.labels[(objectA, objectB)] = relationName

	# Call example: add_relation_from([ ('One','Two'), ('Two','Three') ])
	def add_relation_from(self, relations):
		self.graph.add_edges_from(relations)

	def draw_network(self):
		# nx.draw_networkx(self.graph)
		pos = nx.spring_layout(self.graph, k=0.5, iterations=1000)
		# k controls the distance between the nodes and varies between 0 and 1
    	# iterations is the number of times simulated annealing is run
    	# default k =0.1 and iterations=50

		# nodes
		nx.draw_networkx_nodes(self.graph,pos,node_size=2000, node_color="white")

		# edges
		nx.draw_networkx_edges(self.graph,pos, width=6,alpha=0.5,edge_color='black')

		# labels
		nx.draw_networkx_labels(self.graph,pos,font_size=8,font_family='sans-serif')

		nx.draw_networkx_edge_labels(self.graph,pos, self.labels)

		plt.axis('off')
		plt.show()