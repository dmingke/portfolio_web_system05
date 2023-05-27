#!/usr/bin/env python3
"""Reduce 0."""

# define necessary variables and data structures
import sys
import itertools

def reduce0(key, group):
    group = list(group)
    doc_num = 0
    # Calculate the total number of documents
    for row in group:
        _, temp_doc_num = row.strip().split()
        doc_num += int(temp_doc_num)
    print(f"{doc_num}")

def main():
    groups = itertools.groupby(sys.stdin, lambda x: x.partition("\t")[0])
    for key, group in groups:
        reduce0(key, group)

if __name__ == "__main__":
    main()
