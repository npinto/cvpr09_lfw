#!/usr/bin/env python
# -*- coding: utf-8 -*-

import optparse
from os import path
import numpy as np
import csv

# ------------------------------------------------------------------------------
#DEFAULT_OUTPUT_FNAME_PATTERN = "lfw_view2_pairs_%02d.csv"
DEFAULT_PAIRS_FNAMES = ["pairs_%02d.txt" % (i+1) for i in xrange(10)]

# ------------------------------------------------------------------------------
def lfw_view2_to_csv(output_fname_pattern,
                     pairs_fnames = DEFAULT_PAIRS_FNAMES,                     
                     ):

    splits = []
    for i, pairs_fname in enumerate(pairs_fnames):
        print "Parsing pairs file '%s'" % (pairs_fname)

        pairs_fin = open(pairs_fname)
        pairs_lines = np.array([line.split('\n')[0]
                                for line in pairs_fin.readlines()])
        assert len(pairs_lines) == 1500

        pairs_lines.shape = -1, 5

        pairs_list = []
        for same1, same2, diff1, diff2, _ in pairs_lines:

            assert path.split(same1)[0] == path.split(same2)[0]
            assert path.split(diff1)[0] != path.split(diff2)[0]

            pairs_list += [ (same1, same2, "same") ]
            pairs_list += [ (diff1, diff2, "different") ]

        splits += [pairs_list]

    splits = np.array(splits)
    nsplits = len(splits)    

    csv_rows = []
    idx = np.arange(nsplits)
    for i, sel in enumerate(idx[::-1]):

        # train
        train_sel = idx != sel
        train_list = [tuple(elt)+('train',)
                      for elt in splits[train_sel].reshape(-1,3)]

        # test
        test_sel = idx == sel
        test_list = [tuple(elt)+('test',)
                     for elt in splits[test_sel].reshape(-1,3)]

        assert len(set(train_list) & set(test_list)) == 0

        output_fname = output_fname_pattern % (i+1)
        print "Writing output csv file '%s'" % (output_fname)
        fout = open(output_fname, "w+")
        csvw = csv.writer(fout)
        csvw.writerows(train_list)
        csvw.writerows(test_list)

# ------------------------------------------------------------------------------
def main():
    
    usage = "usage: %prog [options] <output_fname_pattern>"
    usage += "\nExample: %prog lfw_view2_split_%02d.csv"
    parser = optparse.OptionParser(usage=usage)

    parser.add_option(
        "--pairs_fname", "-p",
        metavar="STR", type="str",
        action = "append", dest="pairs_fnames",
        default = None,
        help="[default='%default']")
    
    opts, args = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
    else:

        output_fname_pattern = args[0]

        pairs_fnames = opts.pairs_fnames
        if pairs_fnames is None:           
            pairs_fnames = DEFAULT_PAIRS_FNAMES

        lfw_view2_to_csv(output_fname_pattern,
                         pairs_fnames = pairs_fnames,
                         )

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
