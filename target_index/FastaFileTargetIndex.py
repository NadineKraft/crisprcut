from abc import ABC

from Bio import SeqIO
from Bio.Seq import Seq

from fastadict.FastaDictionary import FastaDictionary
from roi.Roi import Roi
from target.Target import Target
from target_index.TargetIndex import TargetIndex


class FastaFileTargetIndex(TargetIndex, ABC):

    def __init__(self, file_name: str, dictionary: FastaDictionary):
        super().__init__()
        self.file_name = file_name
        self.dictionary = dictionary
        self.fasta = None

    def __enter__(self):
        print("reading fasta file: " + self.file_name)
        self.chromosome_sizes = {}

        self._index_fasta()
        return self

    def _index_fasta(self):
        self.fasta = SeqIO.to_dict(SeqIO.parse(self.file_name, "fasta"))
        for chromosome in self.fasta:
            sequence = str(self.fasta[chromosome].seq)
            self.chromosome_sizes[chromosome] = len(sequence)

    def targets(self, roi: Roi):
        chromosome = self.dictionary.lookup(roi.chromosome)
        sequence = str(self.fasta[chromosome].seq)
        yield from _yield_sorted_sense_targets_for_roi(roi, chromosome, sequence)
        yield from _yield_sorted_antisense_targets_for_roi(roi, chromosome, sequence)

    def chromosome_exists(self, chromosome: str):
        return self.dictionary.lookup(chromosome) is not None

    def chromosome_size(self, chromosome: str):
        return self.chromosome_sizes[self.dictionary.size(chromosome)]

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def _yield_sorted_sense_targets_for_roi(roi: Roi, chromosome: str, sequence: str):
    for index in _yield_sorted_sense_indexes(roi, sequence):
        start = index - 21
        stop = index - 1
        if start >= roi.start and stop + 3 <= roi.stop:
            yield Target(chromosome, start, stop, "+", sequence[start: stop], sequence[start - 4:stop + 6])


def _yield_sorted_antisense_targets_for_roi(roi: Roi, chromosome: str, sequence: str):
    for index in _yield_sorted_antisense_indexes(roi, sequence):
        start = index + 3
        stop = index + 23
        if start - 3 >= roi.start and stop <= roi.stop:
            yield Target(chromosome, start, stop, "-", str(Seq(sequence[start: stop]).complement()),
                         str(Seq(sequence[start - 6: stop + 4]).complement()))


def _yield_sorted_sense_indexes(roi: Roi, sequence: str):
    yield from _yield_all_sense_pam_indexes(roi, sequence, "GG")


def _yield_sorted_antisense_indexes(roi: Roi, sequence: str):
    yield from _yield_all_antisense_pam_indexes(roi, sequence, "CC")


def _yield_all_sense_pam_indexes(roi: Roi, sequence: str, pam: str):
    index = sequence.find(pam, roi.start + 21)
    while -1 < index < roi.stop:
        yield index
        index = sequence.find(pam, index + 1)


def _yield_all_antisense_pam_indexes(roi: Roi, sequence: str, pam: str):
    index = sequence.find(pam, roi.start)
    while -1 < index < roi.stop - 23:
        yield index
        index = sequence.find(pam, index + 1)
