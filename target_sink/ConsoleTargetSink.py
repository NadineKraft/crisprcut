from roi.Roi import Roi
from target.Target import Target
from target_sink.TargetSink import TargetSink


class ConsoleTargetSink(TargetSink):

    def __init__(self):
        super().__init__()

    def append(self, roi: Roi, target: Target, score: float):
        print(
            roi.chromosome
            + " "
            + str(target.start)
            + " "
            + str(target.stop)
            + " "
            + roi.name
            + " "
            + str(score)
            + " "
            + target.strand
            + " "
            + target.sequence
        )
