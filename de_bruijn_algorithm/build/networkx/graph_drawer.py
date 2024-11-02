import networkx as nx
import matplotlib.pyplot as plt
import random

class GraphDrawer:
    def __init__(self, graph, eulerian_paths=None):
        self.graph = graph
        self.eulerian_paths = eulerian_paths

    def draw_graph(self, draw_eulerian=False):
        pos = nx.circular_layout(self.graph)
        plt.figure(figsize=(10, 6))
        nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color="blue", font_size=10,
                font_weight="bold", edge_color="black", font_color="white")
        
        if draw_eulerian and self.eulerian_paths:
            if len(self.eulerian_paths) == 1:
                chosen_path = self.eulerian_paths[0]
            else:
                chosen_path = random.choice(self.eulerian_paths)

            nx.draw_networkx_nodes(self.graph, pos, nodelist=[chosen_path[0][0], chosen_path[-1][1]],
                               node_color="red", node_size=2000)
            edge_order_labels = {}
            original_edge_labels = nx.get_edge_attributes(self.graph, 'label')

            for i, (src, dst) in enumerate(chosen_path):
                nx.draw_networkx_edges(self.graph, pos, edgelist=[(src, dst)], edge_color="red", width=2)
                original_label = original_edge_labels.get((src, dst), "")
                new_order = f"({i + 1})"
                if (src, dst) in edge_order_labels:
                    edge_order_labels[(src, dst)] += new_order
                elif (dst, src) in edge_order_labels:
                    edge_order_labels[(dst, src)] += new_order
                else:
                    edge_order_labels[(src, dst)] = f"{original_label} {new_order}"

            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_order_labels, font_color="red")
        else:
            edge_labels = nx.get_edge_attributes(self.graph, 'label')
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_color="black")

        plt.title("Grafo de De Bruijn")
        plt.show()