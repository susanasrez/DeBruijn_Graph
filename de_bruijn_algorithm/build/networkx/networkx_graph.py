import networkx as nx
import matplotlib.pyplot as plt
from .eulerian_path import EulerianPathFinder
from ..sequence_assembler import SequenceAssembler
from .graph_drawer import GraphDrawer

class NetworkxGraph:

    def __init__(self):
        self.graph = None
        self.graph_drawer = None
        self.eulerian_path_finder = EulerianPathFinder(self.graph)
        self.eulerian_path = None
        self.sequence_assembler = None

    def build_graph(self, dictionary):
        self.graph = nx.DiGraph()
        for prefix, suffix in dictionary.items():
            if len(suffix) > 1:
                for s in suffix:
                    self.graph.add_edge(prefix, s, label=f"{prefix}{s[-1]}")
            else:
                self.graph.add_edge(prefix, suffix[0], label=f"{prefix}{suffix[0][-1]}")
        self.graph_drawer = GraphDrawer(self.graph)
    
    def draw_graph(self, draw_eulerian=False):
        if self.graph_drawer is None:
            raise ValueError("El grafo no ha sido construido.")
        
        self.graph_drawer.eulerian_paths = self.eulerian_path
        self.graph_drawer.draw_graph(draw_eulerian=draw_eulerian)

  
    def get_eulerian_paths(self):
        self.eulerian_path = self.eulerian_path_finder.find_eulerian_path(self.graph)
        if not self.eulerian_path:
            return "No existe camino euleriano."
        
        paths_output = []
        for path_index, path in enumerate(self.eulerian_path, start=1):
            path_str = f'<li>Camino Euleriano {path_index}: {path[0][0]} -> {path[0][1]}'
            for i in range(1, len(path)):
                path_str += f" -> {path[i][1]}"
            path_str += "</li>"
            paths_output.append(path_str)
        
        return ''.join(paths_output)
    
    def get_conditions(self):
        return self.eulerian_path_finder.get_conditions()
    
    def assemble_sequence(self, kmers):
        if self.eulerian_path is None:
            return "Primero debe encontrar el camino euleriano"
        
        self.sequence_assembler = SequenceAssembler(self.eulerian_path, kmers)
        return self.sequence_assembler.assemble_sequence()
    
