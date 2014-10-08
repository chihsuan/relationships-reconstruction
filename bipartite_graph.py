#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import sys

from modules import json_io
from modules import csv_io

def build_bipartite_graph(keyword_dic_file):    
    
    keyword_dic = json_io.read_json(keyword_dic_file)
    pair_bipartite_graph = to_pair(keyword_dic)

def to_pair(keyword_dic):

    pair_bipartite_graph = {}
    for keyword_t in keyword_dic:
        pair_bipartite_graph[keyword_t] =

if __name__=='__main__':
    build_bipartite_graph(sys.argv[1])
