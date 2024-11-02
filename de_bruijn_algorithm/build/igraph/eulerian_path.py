from itertools import product

class EulerianPathFinder:
    def __init__(self, graph, eulerian_paths=[]):
        self.graph = graph
        self.eulerian_paths = eulerian_paths
        self.cycle_conditions = None
        self.path_conditions = None

    def _is_eulerian_cycle(self):
        return self.graph.is_connected() and all(deg % 2 == 0 for deg in self.graph.degree())

    
    def _is_eulerian_path(self):
        in_degrees = self.graph.degree(mode="in")
        out_degrees = self.graph.degree(mode="out")
        
        start_nodes = [i for i in range(len(in_degrees)) if out_degrees[i] - in_degrees[i] == 1]
        end_nodes = [i for i in range(len(out_degrees)) if in_degrees[i] - out_degrees[i] == 1]

        self.path_conditions = "No tiene un camino euleriano porque: \n"

        if len(start_nodes) == 1 and len(end_nodes) == 1:
            self.path_conditions = "El grafo tiene un camino euleriano."
            return True
        else:
            self.path_conditions += " No tiene nodos de inicio y fin válidos para un camino euleriano."

        return False

    def find_eulerian_path(self, graph):
        self.graph = graph
        self.eulerian_paths = []
        if self._is_eulerian_cycle():

            result = self.graph.es.select(mode="ALL")
            print(result)
            return self.eulerian_paths
        elif self._is_eulerian_path():
            self.eulerian_paths = self.find_all_eulerian_paths()
        
        return self.eulerian_paths
    
    def find_all_eulerian_paths(self):
        in_degrees = self.graph.degree(mode="in")
        out_degrees = self.graph.degree(mode="out")

        node_indices = {v["name"]: idx for idx, v in enumerate(self.graph.vs)}
        start_nodes = [node for node in node_indices if out_degrees[node_indices[node]] - in_degrees[node_indices[node]] == 1]
        end_nodes = [node for node in node_indices if in_degrees[node_indices[node]] - out_degrees[node_indices[node]] == 1]

        if len(start_nodes) == 1 and len(end_nodes) == 1:
            self.eulerian_paths.append(self.graph.eulerian_path())
            return self.eulerian_paths
            
        for start, end in product(start_nodes, end_nodes):
            start_idx = node_indices[start]
            end_idx = node_indices[end]

            temp_graph = self.graph.copy()

            all_paths = temp_graph.get_all_simple_paths(start_idx, to=end_idx, mode="out")

            if all_paths:
                longest_path = max(all_paths, key=len)
                longest_path = [(self.graph.vs[longest_path[i]]["name"], self.graph.vs[longest_path[i + 1]]["name"])
                                for i in range(len(longest_path) - 1)]
                self.eulerian_paths.append(longest_path)

        if len(self.eulerian_paths) > 1:
            self.path_conditions = "El grafo tiene múltiples caminos entre los nodos."
        
        return self.eulerian_paths
    
    def get_conditions(self):
        return self.cycle_conditions, self.path_conditions