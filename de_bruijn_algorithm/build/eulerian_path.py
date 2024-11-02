import networkx as nx
import matplotlib.pyplot as plt

class EulerianPathFinder:
    def __init__(self, graph):
        self.graph = graph
        self.eulerian_path = None
        self.cycle_conditions = None
        self.path_conditions = None

    def _is_eulerian_cycle(self):
        in_degrees = dict(self.graph.in_degree())
        out_degrees = dict(self.graph.out_degree())
        self.cycle_conditions = "No es un ciclo euleriano porque: \n"
        
        for node in in_degrees:
            if in_degrees[node] != out_degrees[node]:
                self.cycle_conditions += f" El nodo {node} tiene {in_degrees[node]} aristas de entrada y {out_degrees[node]} aristas de salida. \n"
            
        if nx.is_strongly_connected(self.graph):
            self.cycle_conditions = "El grafo tiene un ciclo euleriano."
            return True
        else:
            self.cycle_conditions += f" El grafo no es fuertemente conexo."
            return False
    
    def _is_eulerian_path(self):

        in_degrees = dict(self.graph.in_degree())
        out_degrees = dict(self.graph.out_degree())
        nodes_equal_degrees = [node for node in in_degrees if in_degrees[node] == out_degrees[node]]

        start_nodes =  [node for node in in_degrees if out_degrees[node] - in_degrees[node] == 1]
        end_nodes = [node for node in out_degrees if in_degrees[node] - out_degrees[node] == 1]

        self.path_conditions = "No tiene un camino euleriano porque: \n"

        if len(start_nodes) == 1 and len(end_nodes) == 1:
            if len(nodes_equal_degrees) == len(self.graph.nodes()) - 2:
                self.path_conditions = "El grafo tiene un camino euleriano."
                return True
            else:
                self.path_conditions += f"  El grafo tiene {len(nodes_equal_degrees)} nodos con igual grado de entrada y salida pero difiere en {len(self.graph.nodes())-2} nodos."
        else:
            # TODO: todos los poishbles
            self.path_conditions += f"  El grafo tiene {len(start_nodes)} posible(s) nodo(s) de inicio y {len(end_nodes)} posible(s) nodo(s) de fin"

        return False

    def find_eulerian_path(self, graph):
        self.graph = graph
        if self._is_eulerian_cycle():
            self.eulerian_path = list(nx.eulerian_circuit(self.graph))
        elif self._is_eulerian_path():
            self.eulerian_path = list(nx.eulerian_path(self.graph))
        else:
            self.eulerian_path = None
        
        return self.eulerian_path

    def get_conditions(self):
        return self.cycle_conditions, self.path_conditions