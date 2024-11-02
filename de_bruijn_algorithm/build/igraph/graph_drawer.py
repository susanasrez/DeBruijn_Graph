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
            "edge_color": "black",
            "edge_label": self.graph.es["label"],
            "vertex_size": 50,
            "vertex_label_size": 20,
            "edge_label_size": 10,
            "bbox": (800, 800),
            "margin": 80
        }
        print(self.eulerian_paths)
        if draw_eulerian and self.eulerian_paths:
            
            if len(self.eulerian_paths) == 1:
                chosen_path = self.eulerian_paths[0]
            else:
                chosen_path = random.choice(self.eulerian_paths)

            path_edges = [(edge[0], edge[1]) for edge in chosen_path]
            self.graph.es["color"] = ["red" if (e.source, e.target) in path_edges else "black" for e in self.graph.es]

        plot_path = "graph.png"
        plot(self.graph, plot_path, layout=layout, **visual_style)
        
        display(Image(filename=plot_path))