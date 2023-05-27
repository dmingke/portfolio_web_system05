#!/usr/bin/env python3
"""Map 2."""
# The first MapReduce job counts the total number of documents in the collection.
# It should read input from input/ and write output to output0.

import sys


for row in sys.stdin:

    word, doc_id, tfik = row.strip().split()

    print(f"{word}\t{doc_id} {tfik}")
