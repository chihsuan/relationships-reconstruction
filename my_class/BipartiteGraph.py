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
                if values['keyword'] not in keyword_roles:
                    keyword_roles[values['keyword']] = {}

                if role in keyword_roles[values['keyword']]:
                    keyword_roles[values['keyword']][role] += values['weight']
                else:
                    keyword_roles[values['keyword']][role] = values['weight']
        
        '''for keyword, roles in keyword_roles.iteritems():
            max_role = max(roles, key=roles.get)
            print keyword, max_role, sorted(roles, key=roles.get)[-1]'''

        self.keyword_roles = keyword_roles
        return keyword_roles
    
    def dominant_pair(self):
        self.get_pair_keywords()
        self.get_keywords_pair()

        if self.keyword_roles == {}:
            return None, None, 0

        role_pair = sorted(self.roles_keyword, key=lambda k :\
                self.key_weight(self.roles_keyword[k]), reverse=True)[0]
        keywords  = self.roles_keyword[role_pair]  
        dominant_keyword = max(keywords, key=keywords.get)
        confidence = self.key_weight(keywords)

        return role_pair, dominant_keyword, keywords[dominant_keyword]

    def get_direction(self, role_pair, keyword):
        role1, role2 =  role_pair.split('-')
        role1_weight = 0
        role2_weight = 0
        for keyword_t, roles in self.single_graph.iteritems():
            if keyword in keyword_t and role1 in roles and role2 in roles:
                if roles[role1]['speaker']:
                    role1_weight += roles[role1]['weight']
                elif roles[role2]['speaker']:
                    role2_weight += roles[role2]['weight']
        
        total_weight = role1_weight + role2_weight
        if total_weight == 0:
            return role1, role2, 0
        
        if role1_weight > role2_weight:
            return role1, role2, role1_weight / total_weight
        elif role1_weight < role2_weight:
            return role2, role1, role2_weight / total_weight 
        else:
            dir_confidenece = 0.5 if confidence != 0 else 0
            return role1, role2, 0.5

    def update_weighting(self, role_pair, keyword):
        for keyword_t, roles in self.pair_graph.iteritems():
            if role_pair in roles:
                for role, value in roles.iteritems():
                    if role != role_pair:
                        role1, role2 = role.split('-')
                        if role1 not in role_pair:
                            value['weight'] += self.single_graph[keyword_t][role1]['weight']
                        else:
                            value['weight'] += self.single_graph[keyword_t][role2]['weight']


    def remove_keyword(self, role_pair, keyword):
        delete_list = []
        for keyword_t, roles in self.pair_graph.iteritems():
            if keyword in keyword_t and role_pair in roles:
                delete_list.append(keyword_t)
        for key in delete_list:
            del self.pair_graph[key]
    
    def remove_edges(self, role_pair, keyword):
        for keyword_t, roles in self.pair_graph.iteritems():
            if keyword in keyword_t and role_pair in roles:
                del self.pair_graph[keyword_t][role_pair]

    def key_weight(self, keyword):
        value = 0.0
        for k, v in keyword.iteritems():
            value += v
        return value
