#/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys

from modules import json_io

from my_class.SocialGraph import SocialGraph
from my_class.BipartiteGraph import BipartiteGraph

def relationship_minig(single_graph_file, pair_graph_file, social_graph_file, dir_file, clip_file):

    single_graph = json_io.read_json(single_graph_file)
    pair_graph = json_io.read_json(pair_graph_file)
    
    bi_graph, social_graph = graph_init(single_graph, pair_graph, social_graph_file, dir_file, clip_file)

    output_graph = {'nodes':[], "links":[]}
    node_dic = {}
    change = True
   # iterator algorithm1
    while change:
        role_pair, dominant_keyword, votes = bi_graph.dominant_pair()
        if role_pair is None:
            break

        source, target, dir_prob = bi_graph.get_direction(role_pair, dominant_keyword)
        valid_tag = valid_checking(social_graph, source, target, dominant_keyword)
        
        if source not in node_dic:
            node_dic[source] = len(node_dic)
            output_graph['nodes'].append({"group": node_dic[source], "name": source, "ID": node_dic[source]})
        if target not in node_dic: 
            node_dic[target] = len(node_dic)
            output_graph['nodes'].append({"group": node_dic[target], "name": target, "ID": node_dic[target]})

        if valid_tag != False and votes >= 1:
            if type(valid_tag) != unicode:
                print source, '-->', dominant_keyword, '-->', target
                add_links(output_graph, source, target, dominant_keyword, votes, node_dic)
                social_graph.relationship_tagging(source, target, dominant_keyword, votes)
            else:
                print source, '-->', valid_tag, '-->', target
                add_links(output_graph, source, target, valid_tag, votes, node_dic)
                social_graph.relationship_tagging(source, target, valid_tag, votes)
            print votes, dir_prob
        
        bi_graph.update_weighting(role_pair, dominant_keyword)
        if valid_tag:
            bi_graph.remove_keyword(role_pair, dominant_keyword)
        else:
            bi_graph.remove_edges(role_pair, dominant_keyword)

    json_io.write_json('output/social_graph.json', output_graph)
    social_graph.clear()
    social_graph.shutdown()

def graph_init(single_graph, pair_graph, social_graph_file, dir_file, clip_file):
    bi_graph = BipartiteGraph(single_graph, pair_graph) 
    social_graph = SocialGraph()
    social_graph.file_to_db(social_graph_file)
    social_graph.load_pattern(dir_file, clip_file)
    return bi_graph, social_graph

def valid_checking(social_graph, source, target, dominant_keyword):

    if social_graph.has_relationship(source, target) \
        or social_graph.has_relationship(target, source):
        valid_tag = False
    else:
        valid_tag = social_graph.pattern_matching(source, target, dominant_keyword)
    return valid_tag

def add_links(graph, source, target, label, votes, node_dic):
    source_id = node_dic[source]
    target_id = node_dic[target]
    graph['links'].append({"source": source_id, "target": target_id, "value": votes,"label": label})

if __name__=='__main__':
    print __doc__
    if len(sys.argv) > 2:
        relationship_minig(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        relationship_minig('output/single_graph.json', 'output/pair_graph.json',\
                'output/social_graph.json', 'input/dir_rel.json', 'input/clip_rel.json')
