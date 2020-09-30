class Target:

    def __init__(self, chromosome: str, start: int, stop: int, strand: str, sequence: str, model_sequence):
        self.chromosome = chromosome
        self.start = start
        self.stop = stop
        self.strand = strand
        self.sequence = sequence
        self.model_sequence = model_sequence

    def __str__(self):
        return self.chromosome + " " + str(self.start) + " " + str(self.stop) + " " + self.strand + " " + self.sequence
