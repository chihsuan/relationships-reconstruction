#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

'''write data to neo4j'''

import sys

from neo4j import GraphDatabase

from modules import json_io
from modules import csv_io

class GraphDB:

    def __init__(self, neo4j_url="graph.db"):
        self.db = GraphDatabase(neo4j_url) 
        self.nodes = {}
        self.rels = []

    def file_to_db(self, data_path):
        data = json_io.read_json(data_path)
    
        with self.db.transaction:
            for source_name, targets in data.iteritems():
                if source_name in self.nodes:
                    source = self.nodes[source_name]
                else:
                    source = self.db.node(name=source_name)
                    self.nodes[source_name] = source
                for target_name in targets:
                    if target_name in self.nodes:
                        target = self.nodes[target_name]
                    else:
                        target = self.db.node(name=target_name) 
                        self.nodes[target_name] = target
                    #for attr, val in targets[target_name].iteritems():
                    self.rels.append(source.knows(target))
            return self.nodes

            
    def pattern_matching(self, source_name, target_name, keyword):
        source = self.nodes[source_name]
        target = self.nodes[target_name]
        q = '''START me=node({s_id}) MATCH (me)-[:knows]->(remote_friend) \
                WHERE me.name = {s_name} RETURN remote_friend'''
        result = self.db.query(q, s_id=source.id ,s_name=source_name)
        
        for result in result:
            for name in result['remote_friend'].values():
                print name

    def relationship_tagging(self, pair, target, keyword):
        pass

    def clear(self):
        with self.db.transaction:
            for rel in self.db.relationships:
                rel.delete()
            for node in self.db.nodes:
                node.delete()

    def shutdown(self):
        self.db.shutdown()
