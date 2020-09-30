from roi.Roi import Roi
from target.Target import Target
from target_sink.TargetSink import TargetSink

import json


class JsonStringTargetSink(TargetSink):

    def __init__(self):
        super().__init__()
        self.index = 0
        self.data = {}

    def __enter__(self):
        print("writing json string")
        self.data['targets'] = []
        return self

    def append(self, roi: Roi, target: Target, score: float):

        self.data['targets'].append({
            'target_id': str(self.next_index()),
            'chromosome': roi.chromosome,
            'start': str(target.start),
            'stop': str(target.stop),
            'score': str(score),
            'strand': str(target.strand),
            'sequence': str(target.sequence),
            'name': str(roi.name)
        })


    def next_index(self):
        index = self.index + 1
        self.index = index
        return index

    def __exit__(self, exc_type, exc_val, exc_tb):
        return json.dumps(self.data, indent=4)

