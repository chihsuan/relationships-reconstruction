#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import sys

import json_io
import csv_io

def to_json(input_file):
    
    csv_data = csv_io.read_csv(input_file)

    relation = {}
    for row in csv_data:
        relation[row[0]] = {}
        for i in range(1, len(row)):
            relation[row[0]][row[i]] = {'know': 1}

    json_io.write_json('output/social_graph.json', relation)

if __name__=='__main__':
    to_json(sys.argv[1])
