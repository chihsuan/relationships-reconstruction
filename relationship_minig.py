#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys

from modules import json_io


def relationship_minig(single_graph_file, pair_graph_file):
    
    single_grpah = json_io.read_json(single_graph_file)
    pair_graph = json_io.read_json(pair_graph_file)
    
    keywords_role(pair_graph)

def roles_keyword(pair_graph):

    roles_keyword = {}
    for keyword_t, roles in pair_graph.iteritems():
        for role, values in roles.iteritems():
            if role not in roles_keyword:
                roles_keyword[role] = {}

            if values['keyword'] in roles_keyword[role]:
                roles_keyword[role][values['keyword']] += values['weight']
            else:
                roles_keyword[role][values['keyword']] = values['weight']

    for role, keywords in roles_keyword.iteritems():
        print role, max(keywords, key=keywords.get)

def keywords_role(pair_graph):

    keyword_roles = {}
    for keyword_t, roles in pair_graph.iteritems():
        for role, values in roles.iteritems():
            if role not in keyword_roles:
                keyword_roles[values['keyword']] = {}

            if role in keyword_roles[values['keyword']]:
                keyword_roles[values['keyword']][role] += values['weight']
            else:
                keyword_roles[values['keyword']][role] = values['weight']

    for keyword, roles in keyword_roles.iteritems():
        print keyword, max(roles, key=roles.get)

if __name__=='__main__':
    if len(sys.argv) > 2:
        relationship_minig(sys.argv[1], sys.argv[2])
    else:
        relationship_minig('output/single_graph.json', 'output/pair_graph.json')
