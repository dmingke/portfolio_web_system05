#!/usr/bin/env python3
"""Map 1."""
# The first MapReduce job counts the total number of documents in the collection.
# It should read input from input/ and write output to output0.

import sys
import csv
import re
# INPUT: row_id, x, y from csv
# Source: pro tip.
csv.field_size_limit(sys.maxsize)

for row in csv.reader(sys.stdin):
    # "<doc_id>","<doc_title>","<doc_body>"
    doc_id, doc_title, doc_body = row

    # Combine both document title and document body by
    # concatenating them, separated by a space.
    concate_item = doc_title + " " + doc_body
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", concate_item)
    word_list = text.casefold().strip().split()
    filtered_list = []
    with open("stopwords.txt", "r") as f:
        stopwords = f.read().strip().split()
        for word in word_list:
            if word not in stopwords:
                filtered_list.append(word)

    for word in filtered_list:
        # 这儿
        print(f"{word} {doc_id}\t{1}")
