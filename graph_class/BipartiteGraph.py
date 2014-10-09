#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys

from neo4jrestclient.client import GraphDatabase

from modules import json_io
from modules import csv_io

class BipartiteGraph:
    
    def __init__(self, single_graph, pair_graph):
        self.single_graph = single_graph
        self.pair_graph = pair_graph

    def get_pair_keywords(self):

        roles_keyword = {}
        for keyword_t, roles in self.pair_graph.iteritems():
            for role, values in roles.iteritems():
                if role not in roles_keyword:
                    roles_keyword[role] = {}

                if values['keyword'] in roles_keyword[role]:
                    roles_keyword[role][values['keyword']] += values['weight']
                else:
                    roles_keyword[role][values['keyword']] = values['weight']

        '''for role, keywords in roles_keyword.iteritems():
            print role, max(keywords, key=keywords.get)'''

        self.roles_keyword = roles_keyword
        return roles_keyword

    def get_keywords_pair(self):

        keyword_roles = {}
        for keyword_t, roles in self.pair_graph.iteritems():
            for role, values in roles.iteritems():
                if role not in keyword_roles:
                    keyword_roles[values['keyword']] = {}

                if role in keyword_roles[values['keyword']]:
                    keyword_roles[values['keyword']][role] += values['weight']
                else:
                    keyword_roles[values['keyword']][role] = values['weight']
        
        '''for keyword, roles in keyword_roles.iteritems():
            max(roles, key=roles.get)'''

        self.keyword_roles = keyword_roles
        return keyword_roles

    def update_weighting(self, valid_tag, pair, keyword):
        pass

