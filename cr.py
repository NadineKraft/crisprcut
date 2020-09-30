# !/usr/bin/env python3
# -*- coding: <utf8> -*-
import argparse

from crispr.Crispr import Crispr
from misc.Color import RED, BLUE, YELLOW, CYAN
from roi_source.BedFileRoiSource import BedFileRoiSource
from roi_source.JsonFileRoiSource import JsonFileRoiSource
from roi_source.JsonStringRoiSource import JsonStringRoiSource
from target_sink.BedFileTargetSink import BedFileTargetSink, Colors
from target_sink.JsonFileTargetSink import JsonFileTargetSink
# from target_sink.JsonStringTargetSink import JsonStringTargetSink
from fastadict.SimpleFastaDictionary import SimpleFastaDictionary
# from fastadict import FastaDictionary
from target_index.FastaFileTargetIndex import FastaFileTargetIndex
from scorer.GcContentScorer import GcContentScorer
from scorer.DoenchScorer import DoenchScorer
from scorer.MitSpecificityScorer import MitSpecificityScorer
from scorer.NewMitScorer import NewMitScorer
from scorer.ConstantScorer import ConstantScorer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find CRISPR-targets")
    parser.add_argument("--fastadict", type=str, help="Input fastadict filename", required=True)
    parser.add_argument("--input_roi", type=str, help="Allowed roi input file types: .bed, .json, _json", required=True)
    parser.add_argument("--scorer", type=str, choices=['GC', 'Doench', 'MIT'],
                        help="Allowed scoring methods: GC, Doench, MIT")
    parser.add_argument("--input roi_type", type=str, choices=['bed', 'json', 'auto'],
                        help="Allowed input types: bed, json, auto", default='auto')
    parser.add_argument("--output", type=str, help="output filename", required=True)
    parser.add_argument("--frame", default='200', type=int, help="frame size")
    parser.add_argument("--score_minimum", default='0.0', type=float,
                        help="Choose a minimum float score to filter the scores")

    args = parser.parse_args()

    fasta = args.fasta
    input_roi = args.input_roi
    output = args.output
    frame = args.frame
    scorer_name = args.scorer
    score_minimum = args.score_minimum

    # TODO: bei choice 'auto' raten aufgrund der datei endung, ansonsten wie scorer

    if input_roi.endswith('.bed'):
        roi_source = BedFileRoiSource(
            input_roi,
            frame
        )
        target_sink = BedFileTargetSink(
            output,
            "CRISPR gDNAs",
            "Found and filtered gDNAs for the input",
            "2",
            Colors(RED, BLUE, YELLOW, CYAN)
        )
    elif input_roi.endswith('.json'):
        roi_source = JsonFileRoiSource(
            input_roi,
            frame
        )
        target_sink = JsonFileTargetSink(
            output
        )
    elif input_roi.endswith('_json'):
        roi_source = JsonStringRoiSource(
            input_roi,
            frame
        )
        # target_sink = JsonStringTargetSink()
        # TODO: JsonStringTargetSink doesn't work yet. Can't access the json dump in app.py
        target_sink = JsonFileTargetSink(
            'GiveMeTargets'
        )

    else:
        print("Wrong roi input file format. Please enter a *.bed or *.json file")

    target_index = FastaFileTargetIndex(
        fasta,
        SimpleFastaDictionary()
    )

    if scorer_name == 'GC':
        scorer = GcContentScorer()
    elif scorer_name == 'Doench':
        scorer = DoenchScorer()
    elif scorer_name == 'MIT':
        #scorer = MitSpecificityScorer()
        scorer = NewMitScorer()
    else:
        print("Using default Constant Scorer")
        scorer = ConstantScorer()

    Crispr(roi_source, target_index, scorer, target_sink, score_minimum).perform()
