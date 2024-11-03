from itertools import product

class EulerianPathFinder:
    def __init__(self, graph, eulerian_paths=[]):
        self.graph = graph
        self.eulerian_paths = eulerian_paths
        self.cycle_conditions = None
        self.path_conditions = None

    def _is_eulerian_cycle(self):
        return self.graph.is_connected() and all(deg % 2 == 0 for deg in self.graph.degree())
    
    def _find_eulerian_cycle(self):
        g_copy = self.graph.copy()
        cycle = []
        stack = [g_copy.vs[0]["name"]]

        while stack:
            v_name = stack[-1]
            v_index = g_copy.vs.find(name=v_name).index 
            if g_copy.degree(v_index, mode="out") > 0:
                next_edge = g_copy.incident(v_index, mode="OUT")[0]
                next_vertex_index = g_copy.es[next_edge].target
                next_vertex_name = g_copy.vs[next_vertex_index]["name"]
                stack.append(next_vertex_name)
                cycle.append((v_name, next_vertex_name))
                g_copy.delete_edges(next_edge)
            else:
                stack.pop()

        return [cycle]

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
            return self._find_eulerian_cycle()
        elif self._is_eulerian_path():
            self.eulerian_paths = self.find_all_eulerian_paths()
        
        return self.find_all_eulerian_paths()
    
    def _deep_search(self, temp_graph, v, path, used_edges, end_idx):
        if len(used_edges) == temp_graph.ecount() and v == end_idx:
            eulerian_path = [(self.graph.vs[src]["name"], self.graph.vs[dst]["name"]) for src, dst in path]
            self.eulerian_paths.append(eulerian_path)
            return
                
        for e in temp_graph.incident(v, mode="OUT"):
            if e not in used_edges:
                next_vertex = temp_graph.es[e].target
                path.append((v, next_vertex))
                used_edges.add(e)
                self._deep_search(temp_graph, next_vertex, path, used_edges, end_idx)
                path.pop()
                used_edges.remove(e)
    
    def find_all_eulerian_paths(self):
        in_degrees = self.graph.degree(mode="in")
        out_degrees = self.graph.degree(mode="out")
        node_indices = {v["name"]: idx for idx, v in enumerate(self.graph.vs)}

        start_nodes = [node for node in node_indices if out_degrees[node_indices[node]] - in_degrees[node_indices[node]] == 1]
        end_nodes = [node for node in node_indices if in_degrees[node_indices[node]] - out_degrees[node_indices[node]] == 1]

        if len(start_nodes) == 1 and len(end_nodes) == 1:
            start_idx = node_indices[start_nodes[0]]
            end_idx = node_indices[end_nodes[0]]
            temp_graph = self.graph.copy()
            self._deep_search(temp_graph, start_idx, [], set(), end_idx)
            self.path_conditions = "El grafo tiene un único camino euleriano."
            return self.eulerian_paths

        for start, end in product(start_nodes, end_nodes):
            start_idx = node_indices[start]
            end_idx = node_indices[end]
            max_path = self._deep_search_longest(start_idx, end_idx)

            if max_path:
                self.eulerian_paths.append(max_path)

        if len(self.eulerian_paths) > 1:
            self.path_conditions += "El grafo tiene múltiples caminos."
        else:
            self.path_conditions = "No existen caminos eulerianos en el grafo dado."

        return self.eulerian_paths

    def _deep_search_longest(self, source, target):
        all_simple_paths = self.graph.get_all_simple_paths(source, to=target)
        if all_simple_paths:
            longest_path = max(all_simple_paths, key=len)
            path_as_edges = [
                (self.graph.vs[longest_path[i]]["name"], self.graph.vs[longest_path[i + 1]]["name"]) 
                for i in range(len(longest_path) - 1)
            ]
            return path_as_edges
        return None
    
    def get_conditions(self):
        return self.cycle_conditions, self.path_conditions