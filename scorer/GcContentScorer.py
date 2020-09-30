from scorer.Scorer import Scorer
from target.Target import Target


class GcContentScorer(Scorer):

    def __init__(self):
        super().__init__()

    def score(self, target: Target):
        target_sequence = list(target.sequence.upper())
        count_gc = target_sequence.count("G") + target_sequence.count("C")
        gc_fraction = float(count_gc) / len(target_sequence)
        gc_content = 100 * gc_fraction
        return float("{0:.2f}".format(gc_content))
