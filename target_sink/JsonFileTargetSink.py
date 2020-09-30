from roi.Roi import Roi
from target.Target import Target
from target_sink.TargetSink import TargetSink

import json


class JsonFileTargetSink(TargetSink):

    def __init__(self, file_name: str):
        super().__init__()
        self.file = None
        self.file_name = file_name
        self.index = 0
        self.data = {}

    def __enter__(self):
        print("writing json file: " + self.file_name)
        self.file = open(self.file_name + '.json', "w+")
        self.data['targets'] = []
        return self

    def append(self, roi: Roi, target: Target, mit_score: float, gc_score: float, doench_score: float):
        self.data['targets'].append({
            'target_id': str(self.next_index()),
            'chromosome': roi.chromosome,
            'start': str(target.start),
            'stop': str(target.stop),
            'mit_score': str(mit_score),
            'gc_score': str(gc_score),
            'doench_score': str(doench_score),
            'strand': str(target.strand),
            'sequence': str(target.sequence),
            'name': str(roi.name)
        })
        # print('json append', self.data['targets'])

    def next_index(self):
        index = self.index + 1
        self.index = index
        return index

    def __exit__(self, exc_type, exc_val, exc_tb):
        json.dump(self.data, self.file, indent=4)
        self.file.close()
