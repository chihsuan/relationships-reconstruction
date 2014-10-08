#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import sys

from modules import json_io
from modules import csv_io

OUTPUT_PATH = 'output/'

def build_bipartite_graph(keyword_dic_file):    
    
    keyword_dic = json_io.read_json(keyword_dic_file)
    pair_bipartite_graph = to_pair(keyword_dic)

    json_io.write_json(OUTPUT_PATH + 'pair_graph.json', pair_bipartite_graph) 

def to_pair(keyword_dic):

    pair_bipartite_graph = {}
    for keyword_t, roles in keyword_dic.iteritems():
        keys = roles.keys()
        if len(roles) >= 2:
            pair_bipartite_graph[keyword_t] = {}
            for i in range(0, len(keys)-1):
                for j in range(i+1, len(keys)):
                    role1 = roles[keys[i]]
                    role2 = roles[keys[j]]
                    pair = keys[i] + '-' + keys[j]
                    pair_bipartite_graph[keyword_t][pair] = {'keyword': role1['keyword'],
                                                             'weight': role1['weight'] + \
                                                                       role2['weight']}
    return pair_bipartite_graph

if __name__=='__main__':
    build_bipartite_graph(sys.argv[1])
