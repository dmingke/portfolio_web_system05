#!/usr/bin/env python3
"""Map 0."""
# The first MapReduce job counts the total number of documents in the collection.
# It should read input from input/ and write output to output0.

import sys
import csv
import os
# INPUT: row_id, x, y from csv
# Source: pro tip.
csv.field_size_limit(sys.maxsize)

KEY = "docs_number"

counter = 0
for _ in csv.reader(sys.stdin):
    counter += 1
print(f"{KEY}\t{counter}")
