
class CreateGraph:

    @staticmethod   
    def create_graph(kmers):
        graph = {}
        
        for mer in kmers:
            prefix = mer[:-1]
            suffix = mer[1:]
            if prefix in graph:
                graph[prefix].append(suffix)
            else:
                graph[prefix] = [suffix]

        return graph