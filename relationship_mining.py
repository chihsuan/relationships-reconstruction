#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys

from modules import json_io

from graph_class.SocialGraph import SocialGraph
from graph_class.BipartiteGraph import BipartiteGraph

def relationship_minig(single_graph_file, pair_graph_file, social_graph_file, dir_file, clip_file):

    # load files
    single_graph = json_io.read_json(single_graph_file)
    pair_graph = json_io.read_json(pair_graph_file)
   
    # class
    bi_graph = BipartiteGraph(single_graph, pair_graph) 
    social_graph = SocialGraph()
    social_graph.file_to_db(social_graph_file)
    social_graph.load_pattern(dir_file, clip_file)

    pair_keywords = bi_graph.get_pair_keywords()

    change = True
    # iterator algorithm
    while change:
        change = False
        # statistic weight
        pair_keywords = bi_graph.get_pair_keywords()
        keyword_pairs = bi_graph.get_keywords_pair()

        for role_pair, keywords in pair_keywords.iteritems():
            top_keyword = max(keywords, key=keywords.get)
            if role_pair == max(keyword_pairs[top_keyword], key=keyword_pairs[top_keyword].get):
                source, target = bi_graph.get_direction(role_pair, top_keyword)
                
                #print source, '-->', top_keyword, '-->', target
                if social_graph.has_relationship(source, target):
                    valid_tag = False
                else:
                    valid_tag = social_graph.pattern_matching(source, target, top_keyword)

                if valid_tag != False:
                    change = True 
                    if type(valid_tag) != unicode:
                        social_graph.relationship_tagging(source, target, top_keyword)
                        print source, '-->', top_keyword, '-->', target
                    else:
                        social_graph.relationship_tagging(source, target, valid_tag)
                        print source, '-->', valid_tag, '-->', target

                bi_graph.remove_edges(role_pair, top_keyword)
                bi_graph.update_weighting(valid_tag,role_pair, top_keyword)


    #social_graph.clear()
    social_graph.shutdown()

if __name__=='__main__':
    if len(sys.argv) > 2:
        relationship_minig(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        relationship_minig('output/single_graph.json', 'output/pair_graph.json',\
                'output/social_graph.json', 'input/dir_rel.json', 'input/clip_rel.json')
