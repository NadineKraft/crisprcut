from roi.Roi import Roi
from target.Target import Target
from target_index.TargetIndex import TargetIndex


class MockTargetIndex(TargetIndex):

    def __init__(self):
        super().__init__()

    def yield_all_roi_targets(self, roi: Roi):
        yield Target(roi.chromosome, 23, 42, roi.strand, "ACGTACGTACGTACGTACGT")

    def chromosome_exists(self, chromosome: str):
        return True

    def chromosome_size(self, chromosome: str):
        return 1000
