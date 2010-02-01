#!/usr/bin/env python
# -*- coding: utf-8 -*-

import optparse
from os import path
import csv

# ------------------------------------------------------------------------------
DEFAULT_TEST_FNAME = 'pairsDevTest.txt'
DEFAULT_TRAIN_FNAME = 'pairsDevTrain.txt'

# ------------------------------------------------------------------------------
def lfw_view1_to_csv(output_fname,
                     train_fname = DEFAULT_TRAIN_FNAME,
                     test_fname = DEFAULT_TEST_FNAME,
                     ):

    print "Parsing train file '%s'" % (train_fname)

    train_fin = open(train_fname)
    train_lines = [line.split('\n')[0] for line in train_fin.readlines()]
    train_npairs = int(train_lines[0])
    assert train_npairs*2 == len(train_lines[1:])

    train_list = []
    for line in train_lines[1:]:
        ls = line.split()
        # same ?
        if len(ls) == 3:
            name = ls[0]
            n1 = int(ls[1])
            n2 = int(ls[2])
            fname1 = path.join(name, "%s_%04d.jpg" % (name, n1))
            fname2 = path.join(name, "%s_%04d.jpg" % (name, n2))
            train_list += [ (fname1, fname2, "same", "train") ]
        # different ?
        elif len(ls) == 4:
            name1 = ls[0]
            n1 = int(ls[1])
            name2 = ls[2]
            n2 = int(ls[3])
            fname1 = path.join(name1, "%s_%04d.jpg" % (name1, n1))
            fname2 = path.join(name2, "%s_%04d.jpg" % (name2, n2))
            train_list += [ (fname1, fname2, "different", "train") ]
        else:
            raise RuntimeError("unexpected error "
                               "when parsing '%s'" % train_fname)

    print "Parsing test file '%s'" % (test_fname)
    test_fin = open(test_fname)
    test_lines = [line.split('\n')[0] for line in test_fin.readlines()]
    test_npairs = int(test_lines[0])
    assert test_npairs*2 == len(test_lines[1:])
    
    test_list = []
    for line in test_lines[1:]:
        ls = line.split()
        # same ?
        if len(ls) == 3:
            name = ls[0]
            n1 = int(ls[1])
            n2 = int(ls[2])
            fname1 = path.join(name, "%s_%04d.jpg" % (name, n1))
            fname2 = path.join(name, "%s_%04d.jpg" % (name, n2))
            test_list += [ (fname1, fname2, "not-same", "test") ]
        # not same ?
        elif len(ls) == 4:
            name1 = ls[0]
            n1 = int(ls[1])
            name2 = ls[2]
            n2 = int(ls[3])
            fname1 = path.join(name1, "%s_%04d.jpg" % (name1, n1))
            fname2 = path.join(name2, "%s_%04d.jpg" % (name2, n2))
            test_list += [ (fname1, fname2, "-1", "test") ]
        else:
            raise RuntimeError("unexpected error "
                               "when parsing '%s'" % test_fname)

    print "Writing output csv file '%s'" % (output_fname)
    fout = open(output_fname, "w+")
    csvw = csv.writer(fout)
    csvw.writerows(train_list)
    csvw.writerows(test_list)

# ------------------------------------------------------------------------------
def main():
    
    usage = "usage: %prog [options] <output_fname>"
    parser = optparse.OptionParser(usage=usage)

    parser.add_option(
        "--train_fname", "-r",
        metavar="STR", type="str",
        default = DEFAULT_TRAIN_FNAME,
        help="[default='%default']")
    
    parser.add_option(
        "--test_fname", "-e",
        metavar="STR", type="str",
        default = DEFAULT_TEST_FNAME,
        help="[default='%default']")

    opts, args = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
    else:

        output_fname = args[0]

        lfw_view1_to_csv(output_fname,
                         train_fname = opts.train_fname,
                         test_fname = opts.test_fname,
                         )


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
