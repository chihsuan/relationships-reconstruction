#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import sys

from modules import json_io
from modules import csv_io

OUTPUT_PATH = 'output/'

def build_bipartite_graph(keyword_dic_file):    
    
    keyword_dic = json_io.read_json(keyword_dic_file)
    keyword_dic = weight_normalize(keyword_dic)
    
    pair_bipartite_graph = to_pair(keyword_dic)

    json_io.write_json(OUTPUT_PATH + 'pair_graph.json', pair_bipartite_graph) 
    json_io.write_json(OUTPUT_PATH + 'single_graph.json', keyword_dic)
    
def weight_normalize(keyword_dic):

    for keyword_t, roles in keyword_dic.iteritems():
        total_weight = 0
        for role, values in roles.iteritems():
            total_weight += values['weight']
        for role, values in roles.iteritems():
            values['weight'] = float(values['weight']) / total_weight

    return keyword_dic

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
                    if keys[i] < keys[j]:
                        pair = keys[i] + '-' + keys[j]
                    else:
                        pair = keys[j] + '-' + keys[i]
                    pair_bipartite_graph[keyword_t][pair] = {'keyword': role1['keyword'],
                                                             'weight': role1['weight'] + \
                                                                       role2['weight']}
    return pair_bipartite_graph

if __name__=='__main__':
    build_bipartite_graph(sys.argv[1])
