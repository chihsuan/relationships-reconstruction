#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys

from modules import json_io
from modules import csv_io
from modules import data_transform


def relation_mining(input_way, relation_file):
    data_transform.to_json(relation_file)

if __name__ == '__main__':
    relation_mining(sys.argv[1], sys.argv[2])

