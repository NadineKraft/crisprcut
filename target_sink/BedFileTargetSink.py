from misc.Color import Color
from roi.Roi import Roi
from target.Target import Target
from target_sink.TargetSink import TargetSink


class Colors:

    def __init__(self, sense_strand_color: Color, antisense_strand_color: Color,
                 sense_target_color: Color, antisense_target_color: Color):
        self.sense_strand_color = sense_strand_color
        self.antisense_strand_color = antisense_strand_color
        self.sense_target_color = sense_target_color
        self.antisense_target_color = antisense_target_color

    def strand_color(self, strand: str):
        return self.sense_strand_color if "+" == strand else self.antisense_strand_color

    def target_color(self, strand: str):
        return self.sense_target_color if "+" == strand else self.antisense_target_color


class BedFileTargetSink(TargetSink):

    def __init__(self, file_name: str, track_name: str, description: str, visibility: str, colors: Colors):
        super().__init__()
        self.file = None
        self.file_name = file_name
        self.track_name = track_name
        self.description = description
        self.visibility = visibility
        self.colors = colors
        self.index = 0

    def __enter__(self):
        print("writing bed file: " + self.file_name)
        self.file = open(self.file_name, "w+")
        self.print_line(
            "track name = \""
            + self.track_name
            + "\" description = \""
            + self.description
            + "\" visibility="
            + self.visibility
            + " colorByStrand=\""
            #+ str(self.colors.strand_color("+"))
            #+ " "
            #+ str(self.colors.strand_color("-"))
            #+ "\""
        )
        return self

    def append(self, roi: Roi, target: Target, mit_score: float, gc_score: float, doench_score: float):
        self.print_line(
            str(roi.chromosome)
            + "\t"
            + str(target.start)
            + "\t"
            + str(target.stop)
            + "\t"
            + str(roi.name)
            + "_"
            + str(self.next_index())
            + "\t"
            + str(mit_score)
            + "\t"
            + str(gc_score)
            + "\t"
            + str(doench_score)
            + "\t"
            + str(target.strand)
            #+ "\t" + str(self.colors.target_color(target.strand))
        )

    def next_index(self):
        index = self.index + 1
        self.index = index
        return index

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def print_line(self, line):
        print("output: " + line)
        self.file.write(line + "\n")
