from roi_source.RoiSource import RoiSource
from scorer.Scorer import Scorer
from target_index.TargetIndex import TargetIndex
from target_sink.TargetSink import TargetSink


class Crispr:

    def __init__(self, roi_source: RoiSource, target_index: TargetIndex, mit_scorer: Scorer, gc_scorer: Scorer,
                 doench_scorer: Scorer,
                 target_sink: TargetSink,
                 score_minimum: int):
        self.roi_source = roi_source
        self.target_index = target_index
        self.mit_scorer = mit_scorer
        self.gc_scorer = gc_scorer
        self.doench_scorer = doench_scorer
        self.target_sink = target_sink
        self.score_minimum = score_minimum

    def perform(self):
        with self.roi_source, self.target_index, self.target_sink:
            for roi in self.roi_source.rois():
                print("processing: " + str(roi))
                if self.target_index.is_acceptable(roi):
                    for target in self.target_index.targets(roi):
                        if self.mit_scorer.score(target) >= self.score_minimum:
                            self.target_sink.append(roi, target, self.mit_scorer.score(target),
                                                    self.gc_scorer.score(target), self.doench_scorer.score(target))

                else:
                    print("ignoring: " + str(roi))
