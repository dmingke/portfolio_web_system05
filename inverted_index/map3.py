#!/usr/bin/env python3
"""Map 3."""
# The first MapReduce job counts the total number of documents in the collection.
# It should read input from input/ and write output to output0.

import sys

for row in sys.stdin:

    word, doc_id, tfik, idfk = row.strip().split()

    print(f"{doc_id}\t{word} {tfik} {idfk}")
