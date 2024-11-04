import random
from igraph import plot
from IPython.display import Image, display

class GraphDrawer:
    def __init__(self, graph, eulerian_paths=None):
        self.graph = graph
        self.eulerian_paths = eulerian_paths

    def draw_graph(self, draw_eulerian=False):
        layout = self.graph.layout("fruchterman_reingold")
        visual_style = {
            "vertex_label": self.graph.vs["name"],
            "vertex_color": "blue",
            "vertex_label_color": "white",
            "edge_label": self.graph.es["label"],
            "vertex_size": 80,
            "vertex_label_size": 25,
            "edge_label_size": 15,
            "bbox": (900, 900),
            "margin": 80
        }

        if draw_eulerian and self.eulerian_paths:
            if len(self.eulerian_paths) == 1:
                chosen_path = self.eulerian_paths[0]
            else:
                chosen_path = random.choice(self.eulerian_paths)

            start_node, end_node = chosen_path[0][0], chosen_path[-1][1]
            visual_style["vertex_color"] = [
                "red" if v["name"] in {start_node, end_node} else "blue" for v in self.graph.vs
            ]

            edge_colors = ["black"] * len(self.graph.es)
            edge_labels = self.graph.es["label"][:] 
            edge_label_colors = ["black"] * len(self.graph.es)

            for i, (src_name, dst_name) in enumerate(chosen_path):
                src_idx = self.graph.vs.find(name=src_name).index
                dst_idx = self.graph.vs.find(name=dst_name).index
                edge_idx = self.graph.get_eid(src_idx, dst_idx)

                edge_colors[edge_idx] = "red"
                edge_label_colors[edge_idx] = "red" 
                original_label = self.graph.es[edge_idx]["label"]
                edge_labels[edge_idx] = f"{original_label} ({i + 1})"

            visual_style["edge_color"] = edge_colors
            visual_style["edge_label"] = edge_labels
            visual_style["edge_label_color"] = edge_label_colors

        plot_path = "graph.png"
        plot(self.graph, plot_path, layout=layout, **visual_style)
        
        display(Image(filename=plot_path))