from .networkx.networkx_graph import NetworkxGraph
from .igraph.igraph_graph import IGraphGraph

class BuildGraph:

    __builders = {
        'NetworkxGraph': NetworkxGraph(),
        'IGraph': IGraphGraph()
    }

    @staticmethod
    def initialize_builder(builder):
        return BuildGraph.__builders[builder]