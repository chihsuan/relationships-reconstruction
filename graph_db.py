#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

'''write data to neo4j'''

import sys

from neo4jrestclient.client import GraphDatabase

from modules import json_io
from modules import csv_io

def neo4j_db(neo4j_url, data_path):

    gdb = GraphDatabase(neo4j_url)
    data = json_io.read_json(data_path)
    roles = {}

    for source_name, targets in data.iteritems():
        source = gdb.nodes.create(name=source_name)
        for target_name in targets:
            if target_name in roles:
                target = roles[target_name]
            else:
                target = gdb.nodes.create(name=target_name) 
                roles[target_name] = target
            for attr in targets[target_name]:
                source.relationships.create(str(attr), target)

if __name__=='__main__':
    neo4j_db("http://localhost:7474/db/data/", sys.argv[1])
