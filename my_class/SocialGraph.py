#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import sys

from neo4j import GraphDatabase

from modules import json_io
from modules import csv_io

class SocialGraph:

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

    def load_pattern(self, dir_file, clip_file):
        self.dir_patterns = json_io.read_json(dir_file)
        self.clip_patterns = json_io.read_json(clip_file)

    def has_relationship(self, source_name, target_name):
        source = self.nodes[source_name]
        target = self.nodes[target_name]

        query = '''start source=node({s_id}) \
                        match (source)-[r]->(target) \
                        where target.name = {t_name} return r'''

        number_rel = self.db.query(query, s_id=source.id, t_name=target_name)['r']
        if len(number_rel) > 1:
            return True
        else:
            return False
        
     
    def pattern_matching(self, source_name, target_name, keyword):
        source = self.nodes[source_name]
        target = self.nodes[target_name]
        
        result = self.dir_query(source, target_name) 
        if result == keyword: 
            return True
        elif result:
            return result
        elif result == False:
            return False

        result = self.dir_query(target, source_name) 
        if result == keyword: 
            return True
        elif result:
            return result
        elif result == False:
            return False


     
        result = self.clip_query(source, target_name) 
        if result == keyword: 
            return True
        elif result:
            return result
        elif result == False:
            return False
        return True

    def dir_query(self, source, target_name):
        dir_query = '''START source=node({s_id}) \
                        MATCH (source)-[r1]->(middleman)-[r2]->(target) \
                        WHERE target.name = {t_name} RETURN r1, r2'''

        results = self.db.query(dir_query, s_id=source.id, t_name=target_name)

        for result in results:
            if 'rel' in result['r1'].keys() and \
                    'rel' in result['r2'].keys():
                relationship1 = result['r1']['rel']
                relationship2 = result['r2']['rel']
                if relationship2 in self.dir_patterns[relationship1]:
                    predict_rel = self.dir_patterns[relationship1][relationship2]
                else:
                    return False

                return predict_rel
                
        return None

    def clip_query(self, source, target_name):
        dir_query = '''START source=node({s_id}) \
                        MATCH (source)-[r1]->(middleman)<-[r2]-(target) \
                        WHERE target.name = {t_name} RETURN r1, r2'''

        results = self.db.query(dir_query, s_id=source.id, t_name=target_name)

        for result in results:
            if 'rel' in result['r1'].keys() and 'rel' in result['r2'].keys():
                relationship1 = result['r1']['rel']
                relationship2 = result['r2']['rel']
                if relationship2 in self.clip_patterns[relationship1]:
                    predict_rel = self.clip_patterns[relationship1][relationship2]
                else:
                    return False
                return predict_rel
                
        return None


    def relationship_tagging(self, source_name, target_name, keyword, confidence):
        source = self.nodes[source_name]
        target = self.nodes[target_name]
        with self.db.transaction:
            relationship = source.knows(target, rel=keyword)
            if confidence <= 2:
                print source_name + ' <-- ' + keyword + ' <-- ' + target_name
                relationship = target.knows(source, rel=keyword)

    def clear(self):
        with self.db.transaction:
            for rel in self.db.relationships:
                rel.delete()
            for node in self.db.nodes:
                node.delete()

    def shutdown(self):
        self.db.shutdown()
