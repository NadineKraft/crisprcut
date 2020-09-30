from misc.Base import Resource
from roi.Roi import Roi
from target.Target import Target


class TargetSink(Resource):

    def __init__(self):
        pass

    def append(self, roi: Roi, target: Target, mit_score: float, gc_score: float, doench_score: float):
        raise NotImplementedError
