from .network_graph import NetworkxGraph

class BuildGraph:

    __builders = {
        'NetworkxGraph': NetworkxGraph()
    }

    @staticmethod
    def initialize_builder(builder):
        return BuildGraph.__builders[builder]