#!/usr/bin/env python3
"""Map 5."""
# The first MapReduce job counts the total number of documents in the collection.
# It should read input from input/ and write output to output0.

import sys

for row in sys.stdin:

    word, idfk, doc_id, tfik, di = row.strip().split()
    doc_id_seg = (int(doc_id)) % 3
    print(f"{doc_id_seg}\t{word} {doc_id} {idfk} {tfik} {di}")
