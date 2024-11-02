
class SequenceAssembler:
    def __init__(self, eulerian_paths):
        self.eulerian_paths = eulerian_paths
        self.dna_sequences = []

    def assemble_sequence(self):
        if not self.eulerian_paths:
            return None

        for path in self.eulerian_paths:
            dna_sequence = path[0][0]
            for _, destination in path:
                dna_sequence += destination[-1]
            self.dna_sequences.append(dna_sequence)

        return self.dna_sequences[0] if len(self.dna_sequences) == 1 else "\n".join(self.dna_sequences)