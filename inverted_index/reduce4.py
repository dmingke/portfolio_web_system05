#!/usr/bin/env python3
"""Reduce 3: Calculate tfik"""

import sys
import itertools


def reduce5(key, group):
    group = list(group)
    # for row in group:
    i = 0
    while i != len(group):
        _, word, doc_id, idfk, tfik, d_sum = group[i].strip().split()
        result = f"{word} \t {idfk} {doc_id} {tfik} {d_sum}"
        if i + 1 < len(group):
            _, word1, doc_id1, _, tfik1, d_sum1 = group[i + 1].strip().split()
            while word == word1:
                result += f" {doc_id1} {tfik1} {d_sum1}"
                # 跳
                i += 1
                if i + 1 >= len(group):
                    break
                else:
                    _, word1, doc_id1, _, tfik1, d_sum1 = group[i + 1].strip().split()
        # 正常++
        i += 1    
        print(result)
        # # print(f"{word} \t {idfk} {doc_id} {tfik} {d_sum}") # #        

def main():
    """Divide sorted lines into groups that share a key.
    Docs: https://docs.python.org/3/library/itertools.html#itertools.groupby
    """
    groups = itertools.groupby(sys.stdin, lambda x: x.partition("\t")[0])
    for key, group in groups:
        reduce5(key, group)

if __name__ == "__main__":
    main()
