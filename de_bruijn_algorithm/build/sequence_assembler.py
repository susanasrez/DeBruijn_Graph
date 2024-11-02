
class SequenceAssembler:
    def __init__(self, eulerian_path):
        self.eulerian_path = eulerian_path
        self.dna_sequence = None

    def assemble_sequence(self):
        if self.eulerian_path is None:
            return None

        dna_sequence = self.eulerian_path[0][0]

        for _, destination in self.eulerian_path:
            dna_sequence += destination[-1]

        self.dna_sequence = dna_sequence
        return self.dna_sequence