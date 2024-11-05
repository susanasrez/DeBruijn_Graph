class SequenceAssembler:
    def __init__(self, eulerian_paths, kmers):
        self.eulerian_paths = eulerian_paths
        self.kmers = kmers
        self.dna_sequences = []

    def assemble_sequence(self):
        if not self.eulerian_paths:
            return None

        for path in self.eulerian_paths:
            dna_sequence = path[0][0]
            for _, destination in path:
                dna_sequence += destination[-1]
            self.dna_sequences.append(dna_sequence)
        
        if len(self.dna_sequences) == 1:
            return self.dna_sequences[0]
        
        else:
            longest_sequence = max(self.dna_sequences, key=len)
            possible_sequences = self.align_kmers_with_gaps(longest_sequence)
            return "Secuencia posible: " + possible_sequences


    def align_kmers_with_gaps(self, sequence):
        kmers_in_sequence = self.all_kmers_sequence(sequence)
        kmers_not_in_sequence = list(set(self.kmers) - set(kmers_in_sequence))
        overlap_kmers = self.superpose_kmers(kmers_not_in_sequence)
        k = len(self.kmers[0]) -1

        result = sequence
        while overlap_kmers:
            suffix = result[len(result)-k:]
            matched_kmer = None

            for kmer in overlap_kmers:
                overlap = self.check_prefix(suffix, kmer, k)
                if overlap:
                    matched_kmer = kmer
                    break

            if matched_kmer:
                overlap = self.find_overlap(result, matched_kmer)
                result += matched_kmer[overlap:]
                
                overlap_kmers.remove(matched_kmer)
            else:
                result += '-' + overlap_kmers[0]
                overlap_kmers.pop(0)

        return result
    
    def check_prefix(self, suffix, kmer, k):
        prefix = kmer[:k]
        if suffix == prefix:
            return True
        return False

    
    def all_kmers_sequence(self, sequence):
        kmers_in_sequence = []
        for kmer in self.kmers:
            if kmer in sequence:
                kmers_in_sequence.append(kmer)
        return kmers_in_sequence

    def superpose_kmers(self, kmers_not_in_sequence):
        superposed_kmers = []
        unmatched_kmers = kmers_not_in_sequence[:]

        while unmatched_kmers:
            kmer1 = unmatched_kmers.pop(0)
            matched = False

            for kmer2 in unmatched_kmers[:]:
                overlap = self.find_overlap(kmer1, kmer2)

                if overlap:
                    new_kmer = kmer1 + kmer2[overlap:]
                    superposed_kmers.append(new_kmer)
                    unmatched_kmers.remove(kmer2)
                    matched = True
                    break 

            if not matched:
                superposed_kmers.append(kmer1)

        return superposed_kmers


    def find_overlap(self, kmer1, kmer2):
        max_overlap = min(len(kmer1), len(kmer2)) - 1

        for i in range(max_overlap, 0, -1):
            if kmer1[-i:] == kmer2[:i]:
                return i

        return 0