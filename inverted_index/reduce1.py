#!/usr/bin/env python3
"""Reduce 1: Calculate tfik"""

import sys
import itertools


def reduce1(key, group):
    group = list(group)

    # calculate tfik
    tfik = 0
    for line in group:
        word, doc_id, i = line.strip().split()
        tfik += int(i)
    # 这儿
    print(f"{word}\t{doc_id} {tfik}")


def main():
    """Divide sorted lines into groups that share a key.
    Docs: https://docs.python.org/3/library/itertools.html#itertools.groupby
    """
    groups = itertools.groupby(sys.stdin, lambda x: x.partition("\t")[0])
    for key, group in groups:
        reduce1(key, group)


if __name__ == "__main__":
    main()



