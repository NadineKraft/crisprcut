class Roi:

    def __init__(self, chromosome: str, start: int, stop: int, name: str, score: float, strand: str):
        self.chromosome = chromosome
        self.start = start
        self.stop = stop
        self.name = name
        self.score = score
        self.strand = strand

    def __str__(self):
        return self.chromosome + " " + str(self.start) + " " + str(self.stop) + " " + str(self.name) + " " + str(self.score)
