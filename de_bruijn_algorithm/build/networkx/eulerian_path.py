import networkx as nx
import matplotlib.pyplot as plt
from itertools import product

class EulerianPathFinder:
    def __init__(self, graph, eulerian_paths=[]):
        self.graph = graph
        self.eulerian_paths = eulerian_paths
        self.cycle_conditions = None
        self.path_conditions = None

    def _is_eulerian_cycle(self):
        in_degrees = dict(self.graph.in_degree())
        out_degrees = dict(self.graph.out_degree())
        self.cycle_conditions = "<h3> No tiene un ciclo euleriano porque: </h3>"
        
        for node in in_degrees:
            if in_degrees[node] != out_degrees[node]:
                self.cycle_conditions += f" <li> El nodo {node} tiene {in_degrees[node]} aristas de entrada y {out_degrees[node]} aristas de salida. </li>"
            
        if nx.is_strongly_connected(self.graph):
            self.cycle_conditions = "<h3> El grafo tiene un ciclo euleriano. </h3>"
            self.path_conditions = "<h3>No tiene un camino euleriano porque ya tiene un ciclo euleriano. </h3>"
            return True
        else:
            self.cycle_conditions += " <li> El grafo no es fuertemente conexo. </li>"
            return False
    
    def _is_eulerian_path(self):

        in_degrees = dict(self.graph.in_degree())
        out_degrees = dict(self.graph.out_degree())
        nodes_equal_degrees = [node for node in in_degrees if in_degrees[node] == out_degrees[node]]

        start_nodes =  [node for node in in_degrees if out_degrees[node] - in_degrees[node] == 1]
        end_nodes = [node for node in out_degrees if in_degrees[node] - out_degrees[node] == 1]

        self.path_conditions = "<h3> No tiene un camino euleriano porque: </h3>"

        if len(start_nodes) == 1 and len(end_nodes) == 1:
            if len(nodes_equal_degrees) == len(self.graph.nodes()) - 2:
                self.path_conditions = "<h3> El grafo tiene un camino euleriano. </h3>"
                return True
            else:
                self.path_conditions += f"  <li> El grafo tiene {len(nodes_equal_degrees)} nodos con igual grado de entrada y salida pero difiere en {len(self.graph.nodes())-2} nodos.</li>"
        elif len(start_nodes) > 1 or len(end_nodes) > 1:
            self.path_conditions += f" <li> El grafo tiene {len(start_nodes)} posible(s) nodo(s) de inicio y {len(end_nodes)} posible(s) nodo(s) de fin.</li>"
            return len(start_nodes) > 0 and len(end_nodes) > 0
        else:
            self.path_conditions += " <li> No tiene nodos de inicio y fin válidos para un camino euleriano. </li>"

        return False

    def find_eulerian_path(self, graph):
        self.graph = graph
        self.eulerian_paths = []
        if self._is_eulerian_cycle():
            self.eulerian_paths = [list(nx.eulerian_circuit(self.graph))]
            return self.eulerian_paths
        elif self._is_eulerian_path():
            self.eulerian_paths = self.find_all_eulerian_paths()
        
        return self.eulerian_paths
    
    def find_all_eulerian_paths(self):
        in_degrees = dict(self.graph.in_degree())
        out_degrees = dict(self.graph.out_degree())

        start_nodes = [node for node in in_degrees if out_degrees[node] - in_degrees[node] == 1]
        end_nodes = [node for node in out_degrees if in_degrees[node] - out_degrees[node] == 1]

        if len(start_nodes) == 1 and len(end_nodes) == 1:
            self.eulerian_paths.append(list(nx.eulerian_path(self.graph)))
            return self.eulerian_paths

        for start, end in product(start_nodes, end_nodes):

            temp_graph = self.graph.copy()
            eulerian_path = list(nx.all_simple_paths(temp_graph, source=start, target=end))

            longest_path = max(eulerian_path, key=len)

            longest_path = [(longest_path[i], longest_path[i + 1]) for i in range(len(longest_path) - 1)]
            self.eulerian_paths.append(longest_path)


        if len(self.eulerian_paths) > 1:
            self.path_conditions = "<h3> El grafo tiene múltiples caminos entre los nodos. </h3>"
        return self.eulerian_paths
    
    def get_conditions(self):
        return self.cycle_conditions, self.path_conditions