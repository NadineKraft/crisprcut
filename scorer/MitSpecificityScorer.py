from scorer.Scorer import Scorer
from target.Target import Target

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="crisprapp"
)

mycursor = mydb.cursor()


class MitSpecificityScorer(Scorer):

    def __init__(self):
        super().__init__()

        self.dictionary = {
            "NC_000001.11": "chr1",
            "NC_000002.12": "chr2",
            "NC_000003.12": "chr3",
            "NC_000004.12": "chr4",
            "NC_000005.10": "chr5",
            "NC_000006.12": "chr6",
            "NC_000007.14": "chr7",
            "NC_000008.11": "chr8",
            "NC_000009.12": "chr9",
            "NC_000010.11": "chr10",
            "NC_000011.10": "chr11",
            "NC_000012.12": "chr12",
            "NC_000013.11": "chr13",
            "NC_000014.9": "chr14",
            "NC_000015.10": "chr15",
            "NC_000016.10": "chr16",
            "NC_000017.11": "chr17",
            "NC_000018.10": "chr18",
            "NC_000019.10": "chr19",
            "NC_000020.11": "chr20",
            "NC_000021.9": "chr21",
            "NC_000022.11": "chr22",
            "NC_000023.11": "chrX",
            "NC_000024.10": "chrY",
        }

    def score(self, target: Target):
        self.chromosome = self.dictionary.get(target.chromosome)
        self.strand = target.strand
        if self.strand == '-':
            self.start = target.start - 3

        else:
            self.start = target.start

        try:
            mycursor.execute("SELECT * FROM scores WHERE chromosome=%s AND start=%s", (self.chromosome, self.start))
            db_line = mycursor.fetchall()
            if db_line:
                mit_score = db_line[0][4]
            else:
                mit_score = 0
            return int(mit_score)

        except StopIteration:
            raise ValueError("No matching record found")


''' 
For each off-target, the probability of being a true secondary target for Cas9 is estimated as described in Optimized 
CRISPR Design tool (Zhang Lab, MIT)
A score S_off is calculated for each off-target based on the number and position of the mismatches.
The higher the score, the higher the probability of acting as true secondary Cas9 site.
In general, for Cas ß mismatches at last postions ( close to the PAM) strongly decrease the off-target's score.

Source code from https://github.com/maximilianh/crisporWebsite/blob/master/crispor.py
'''

'''
HIT_SCORE_MATRIX = [0, 0, 0.014, 0, 0, 0.395, 0.317, 0, 0.389, 0.079, 0.445, 0.508, 0.613, 0.851, 0.732, 0.828, 0.615,
                    0.804, 0.685, 0.583]


class MitSpecificityScorer(Scorer):

    def __init__(self):
        super().__init__()

    def score(self, target: Target):
        return 4

    def calc_hit_score(self, string1, string2):
        # The Patrick Hsu weighting scheme
        # S. aureus requires 21bp long guides. We fudge by using only last 20bp
        dists = []  # distances between mismatches, for part 2
        mm_count = 0  # number of mismatches, for part 3
        last_mm_pos = None  # position of last mismatch, used to calculate distance

        score1 = 1.0
        for pos in range(0, len(string1)):
            if string1[pos] != string2[pos]:
                mm_count += 1
                if not None == last_mm_pos:
                    dists.append(pos - last_mm_pos)
                score1 *= 1 - HIT_SCORE_MATRIX[pos]
                last_mm_pos = pos
        # 2nd part of the score
        if mm_count < 2:  # special case, not shown in the paper
            score2 = 1.0
        else:
            avg_dist = sum(dists) / len(dists)
            score2 = 1.0 / (((19 - avg_dist) / 19.0) * 4 + 1)
        # 3rd part of the score
        if mm_count == 0:  # special case, not shown in the paper
            score3 = 1.0
        else:
            score3 = 1.0 / (mm_count ** 2)

        score = score1 * score2 * score3 * 100
        return score

    def calc_mit_guide_score(self, hitSum):
        """ Sguide defined on http://crispr.mit.edu/about
        Input is the sum of all off-target hit scores. Returns the specificity of the guide.
        """
        score = 100 / (100 + hitSum)
        score = int(round(score * 100))
        return score'''
