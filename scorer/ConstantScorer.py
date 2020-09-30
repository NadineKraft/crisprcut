from scorer.Scorer import Scorer
from target.Target import Target


class ConstantScorer(Scorer):

    def __init__(self):
        super().__init__()

    def score(self, target: Target):
        return 1
