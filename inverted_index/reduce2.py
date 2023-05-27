#!/usr/bin/env python3
"""Reduce 2: Calculate idfk"""

import sys
import itertools
import math


def reduce2(key, group, num_doc):
    group = list(group)

    # calculate tfik
    nk = 0
    tfik = -1
    doc_id = -1
    nk = len(group)
    idfk = float(math.log10(num_doc/nk))
    for row in group:
        word, doc_id, tfik = row.strip().split()
        print(f"{word}\t {doc_id} {tfik} {idfk}")


def main():
    """Divide sorted lines into groups that share a key.
    Docs: https://docs.python.org/3/library/itertools.html#itertools.groupby
    """
    groups = itertools.groupby(sys.stdin, lambda x: x.partition("\t")[0])
    num_doc = int(open("total_document_count.txt", "r").read())
    for key, group in groups:
        reduce2(key, group, num_doc)
    

if __name__ == "__main__":
    main()
