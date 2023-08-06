import networkx as nx

class Node:
    def __init__(self, name, connections):#atributos del nodo
        self.name = name
        self.connections = connections
        self.graph = None

    def create_graph(self):#grafo para el nodo
        self.graph = nx.DiGraph()
        self.graph.add_node(self.name)
        for node, prob in self.connections.items():
            self.graph.add_node(node)
            self.graph.add_edge(self.name, node, weight=prob)

    def set_probability(self, connection, probability):#conexiones con probabilidades
        if connection in self.connections:
            self.connections[connection] = probability
            if self.graph is not None:
                self.graph[self.name][connection]['weight'] = probability

    def get_probability(self, connection):
        if connection in self.connections:
            return self.connections[connection]
        return None

    def get_connections(self):
        return list(self.connections.keys())

    def get_graph(self):
        if self.graph is None:
            self.create_graph()
        return self.graph

class BayesianNetwork:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        if node.name not in self.nodes:
            self.nodes[node.name] = node
        else:
            print("El nodo con este nombre ya existe.")

    def is_completely_described(self):
        for node in self.nodes.values():
            for connection in node.get_connections():
                if node.get_probability(connection) is None:
                    return False
        return True