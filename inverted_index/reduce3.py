#!/usr/bin/env python3
"""Reduce 3: Calculate tfik"""

import sys
import itertools
import math


def reduce3(key, group):
    group = list(group)
    di = 0
    # calculate the normalization factor
    for row in group:
        doc_id, word, tfik, idfk = row.strip().split()
        di += float(pow(float(tfik) * float(idfk),2))
    for row in group:
        doc_id, word, tfik, idfk = row.strip().split()
        print(f"{word}\t {idfk} {doc_id} {tfik} {di}")

def main():
    """Divide sorted lines into groups that share a key.
    Docs: https://docs.python.org/3/library/itertools.html#itertools.groupby
    """
    groups = itertools.groupby(sys.stdin, lambda x: x.partition("\t")[0])
    for key, group in groups:
        reduce3(key, group)


if __name__ == "__main__":
    main()
