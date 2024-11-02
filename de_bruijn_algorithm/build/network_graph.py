import networkx as nx
import matplotlib.pyplot as plt
from .eulerian_path import EulerianPathFinder
from .sequence_assembler import SequenceAssembler
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
        
        self.graph_drawer.eulerian_path = self.eulerian_path
        self.graph_drawer.draw_graph(draw_eulerian=draw_eulerian)

  
    def get_eulerian_path(self):
        self.eulerian_path = self.eulerian_path_finder.find_eulerian_path(self.graph)
        if not self.eulerian_path:
            return "No existe camino euleriano"
        
        path = f'{self.eulerian_path[0][0]} -> {self.eulerian_path[0][1]}'
        for i in range(1, len(self.eulerian_path)):
            path += f" -> {self.eulerian_path[i][1]}"
        return path
    
    def get_conditions(self):
        return self.eulerian_path_finder.get_conditions()
    
    def assemble_sequence(self):
        if self.eulerian_path is None:
            return "Primero debe encontrar el camino euleriano"
        
        self.sequence_assembler = SequenceAssembler(self.eulerian_path)
        return self.sequence_assembler.assemble_sequence()
    
