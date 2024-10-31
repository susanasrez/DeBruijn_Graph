import networkx as nx
import matplotlib.pyplot as plt

class NetworkxGraph:

    def __init__(self):
        self.graph = nx.DiGraph()
        self.eulerian_path = None
        self.dna_sequence = None

    def build_graph(self, dictionary):

        for prefix, sufix in dictionary.items():
            if len(sufix) > 1:
                for s in sufix:
                    self.graph.add_edge(prefix, s, label=f"{prefix}{s[-1]}")
            else:
                self.graph.add_edge(prefix, sufix[0], label=f"{prefix}{sufix[0][-1]}")
    
    def draw_graph(self, draw_eulerian=False ):
        authomatic_pos = nx.circular_layout(self.graph)
        plt.figure(figsize=(10, 6))
        nx.draw(self.graph, authomatic_pos, with_labels=True, node_size=2000, node_color="blue", font_size=10, font_weight="bold", edge_color="black", font_color="white")

        if draw_eulerian and self.eulerian_path:
            nx.draw_networkx_nodes(self.graph, authomatic_pos, nodelist=[self.eulerian_path[0][0], self.eulerian_path[-1][1]], node_color="red", node_size=2000)
            edge_order_labels = {}
            original_edge_labels = nx.get_edge_attributes(self.graph, 'label')
        
            for i, (src, dst) in enumerate(self.eulerian_path):
                nx.draw_networkx_edges(self.graph, authomatic_pos, edgelist=[(src, dst)], 
                                    edge_color="red", width=2)
                
                original_label = original_edge_labels.get((src, dst), "")
                new_order = f"({i + 1})"
                if (src, dst) in edge_order_labels:
                    edge_order_labels[(src, dst)] += new_order

                elif (dst, src) in edge_order_labels:
                    edge_order_labels[(dst, src)] += new_order
                else:
                    edge_order_labels[(src, dst)] = f"{original_label} {new_order}"

            nx.draw_networkx_edge_labels(self.graph, authomatic_pos, edge_labels=edge_order_labels, font_color="red")

        if not draw_eulerian or self.eulerian_path is None:
            edge_labels = nx.get_edge_attributes(self.graph, 'label')
            nx.draw_networkx_edge_labels(self.graph, authomatic_pos, edge_labels=edge_labels, font_color="black")
        plt.title("Grafo de De Bruijn")
        plt.show()
    
    def _is_eulerian_cycle(self):
        in_degrees = dict(self.graph.in_degree())
        out_degrees = dict(self.graph.out_degree())
        
        for node in in_degrees:
            if in_degrees[node] != out_degrees[node]:
                return False
            
        if nx.is_strongly_connected(self.graph):
            return True
        else:
            return False
    
    def _is_eulerian_path(self):

        in_degrees = dict(self.graph.in_degree())
        out_degrees = dict(self.graph.out_degree())
        nodes_equal_degrees = [node for node in in_degrees if in_degrees[node] == out_degrees[node]]

        start_nodes =  [node for node in in_degrees if out_degrees[node] - in_degrees[node] == 1]
        end_nodes = [node for node in out_degrees if in_degrees[node] - out_degrees[node] == 1]

        if len(start_nodes) == 1 and len(end_nodes) == 1:
            if len(nodes_equal_degrees) == len(self.graph.nodes()) - 2:
                return True
        return False

    def _find_eulerian_path(self):
        if self._is_eulerian_cycle():
            self.eulerian_path = list(nx.eulerian_circuit(self.graph))
        elif self._is_eulerian_path():
            self.eulerian_path = list(nx.eulerian_path(self.graph))
        else:
            self.eulerian_path = None
        
        return self.eulerian_path
    
    def get_eulerian_path(self):
        caclculate_path = self._find_eulerian_path()
        if caclculate_path is None:
            return "No existe camino euleriano"
        
        path = f'{self.eulerian_path[0][0]} -> {self.eulerian_path[0][1]}'

        for i in range(1, len(self.eulerian_path)):
            path += f" -> {self.eulerian_path[i][1]}"

        return path
    
    def assemble_sequence(self):
        if self.eulerian_path is None:
            return None
        
        self.dna_sequence = self.eulerian_path[0][0]

        for _, destination in self.eulerian_path:
            self.dna_sequence += destination[-1]

        return self.dna_sequence
    
