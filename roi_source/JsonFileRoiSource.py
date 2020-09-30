import json
from roi.Roi import Roi
from roi_source.RoiSource import RoiSource


class Entry:

    def __init__(self, chromosome: str, start: int, stop: int, name: str, score: float, strand: str, full_region: bool):
        self.chromosome = chromosome
        self.start = start
        self.stop = stop
        self.name = name
        self.score = score
        self.strand = strand
        self.full_region = full_region

    def to_rois(self, frame_size: int):
        if self.full_region:
            yield self.to_full_roi(frame_size)
        else:
            yield self.to_downstream_roi(frame_size)
            yield self.to_upstream_roi(frame_size)

    def to_full_roi(self, frame_size: int):
        return Roi(
            self.chromosome,
            self.start - frame_size,
            self.stop + frame_size,
            self.name,
            self.score,
            self.strand
        )

    def to_downstream_roi(self, frame_size: int):
        return Roi(
            self.chromosome,
            self.start - frame_size,
            self.start,
            self.name,
            self.score,
            self.strand
        )

    def to_upstream_roi(self, frame_size: int):
        return Roi(
            self.chromosome,
            self.stop,
            self.stop + frame_size,
            self.name,
            self.score,
            self.strand
        )

    @staticmethod
    def from_json_entry(string: str):
        chromosome = string['chromosome']
        start = int(string['start'])
        stop = int(string['stop'])
        name = string['name']
        score = float(string['score'])
        strand = string['strand']
        full_region = "1" == string['full_region']

        return Entry(chromosome, start, stop, name, score, strand, full_region)


class JsonFileRoiSource(RoiSource):

    def __init__(self, file_name: str, frame_size: int):
        super().__init__()
        self.file = None
        self.file_name = file_name
        self.frame_size = frame_size

    def __enter__(self):
        print("reading json file: " + self.file_name)
        self.file = open(self.file_name, "rb")
        return self

    def rois(self):
        json_data = json.load(self.file)
        for json_object in json_data['rois']:
            entry = Entry.from_json_entry(json_object)
            yield from entry.to_rois(self.frame_size)


def __exit__(self, exc_type, exc_val, exc_tb):
    self.file.close()
