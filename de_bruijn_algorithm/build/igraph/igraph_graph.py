from .eulerian_path import EulerianPathFinder
from .graph_drawer import GraphDrawer
from ..sequence_assembler import SequenceAssembler
from igraph import Graph

class IGraphGraph:

    def __init__(self):
        self.graph = None
        self.graph_drawer = None
        self.eulerian_path_finder = EulerianPathFinder(self.graph)
        self.eulerian_path = None
        self.sequence_assembler = None

    def build_graph(self, dictionary):
        self.graph = Graph(directed=True)
        nodes = set(dictionary.keys()).union(*dictionary.values())
        self.graph.add_vertices(list(nodes))
        
        edges = []
        labels = []
        
        for prefix, suffixes in dictionary.items():
            for suffix in suffixes:
                edges.append((prefix, suffix))
                labels.append(f"{prefix}{suffix[-1]}")
        
        self.graph.add_edges(edges)
        self.graph.es["label"] = labels

        self.graph_drawer = GraphDrawer(self.graph)
    
    def draw_graph(self, draw_eulerian=False):
        if self.graph_drawer is None:
            raise ValueError("El grafo no ha sido construido.")
        self.graph_drawer.eulerian_paths = self.eulerian_path
        self.graph_drawer.draw_graph(draw_eulerian=draw_eulerian)

    def get_eulerian_paths(self):
        self.eulerian_path = self.eulerian_path_finder.find_eulerian_path(self.graph)
        if not self.eulerian_path:
            return "No existe camino euleriano"
        
        paths_output = []
        for path_index, path in enumerate(self.eulerian_path, start=1):
            path_str = f'<li> Camino Euleriano {path_index}: {path[0][0]} -> {path[0][1]}'
            for i in range(1, len(path)):
                path_str += f" -> {path[i][1]}"
            path_str += "</li>"
            paths_output.append(path_str)
        
        return "".join(paths_output)
    
    def get_conditions(self):
        return self.eulerian_path_finder.get_conditions()
    
    def assemble_sequence(self, kmers):
        if self.eulerian_path is None:
            return "Primero debe encontrar el camino euleriano"
        
        self.sequence_assembler = SequenceAssembler(self.eulerian_path, kmers)
        return self.sequence_assembler.assemble_sequence()