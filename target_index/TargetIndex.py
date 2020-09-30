from misc.Base import Resource
from roi.Roi import Roi


class TargetIndex(Resource):

    def __init__(self):
        pass

    def targets(self, roi: Roi):
        raise NotImplementedError

    def yield_all_roi_targets(self, roi: Roi):
        raise NotImplementedError

    def is_acceptable(self, roi: Roi):
        acceptable = True
        if not self.chromosome_exists(roi.chromosome):
            acceptable = False
            print(
                "info: chromosome "
                + str(roi.chromosome)
                + " is not indexed"
            )
        if roi.start < 0:
            acceptable = False
            print(
                "info: start index "
                + str(roi.start)
                + " is smaller than zero"
            )
        if roi.stop < roi.start:
            acceptable = False
            print(
                "info: stop index "
                + str(roi.stop)
                + " is smaller than start index "
                + str(roi.start)
            )
        if roi.stop > self.chromosome_size(roi.chromosome):
            acceptable = False
            print(
                "info: stop index "
                + str(roi.stop)
                + " is larger than chromosome size"
                + self.chromosome_size(roi.chromosome)
            )
        return acceptable

    def chromosome_exists(self, chromosome):
        raise NotImplementedError

    def chromosome_size(self, chromosome):
        raise NotImplementedError
