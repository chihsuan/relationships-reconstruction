#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

'''
This module is to search keywords in move subtitle.

Define Keyword: keyword are relationships.
ex: Dad

Intput: -> 1 realationship_file 2. subtitle_file
Output: keyword to time in subtitle and keyword_list 
        -> 1.statistics_result_csv_file 2. keyword_list
'''

import sys
import re
from collections import Counter

from modules import csv_io
from modules import time_format

OUTPUT_ROOT_PATH = 'output/'

def keyword_statistics(relationship_file, subtitle_file):
    
    relation_list = csv_io.read_csv(relationship_file)
    subtitle = read_subtitle_file(subtitle_file)

    relation_patterns = {}
    for relation in relation_list:
        '''relation_patterns[relation] = '(^' + relation.lower() + '[,|\.|\?|\!].*)|' + \
                                        '(?<!(\sher|\shis|\sour|heir|your))\s+' + relation.lower() + "[\.|,|\?|!|>]" '''
        relation_patterns[relation] = '(^' + relation.lower() + '[,|\.|\?|\!].*)|' + \
                                        '(?<!(her|his|our|eir|our|\smy|.\sa))\s+' + relation.lower() + "[\.|,|\?|!|>]" 
        
    subtitle_interval = []
    time_to_keyword = []
    keyword_list = []
    for line in subtitle:
        if line.strip():
            subtitle_interval.append(line)
            if len(subtitle_interval) < 2:
                continue

            if len(subtitle_interval) == 2:
                subtitle_time = line[:-2]
                continue
            
            time_to_keyword, keyword_list = keyword_matching(relation_patterns, line, subtitle_time,\
                                                             time_to_keyword, keyword_list)
        else:
            subtitle_interval=[]

    frame_to_keyword = to_frame_keyword(time_to_keyword)

    csv_io.write_csv(OUTPUT_ROOT_PATH + 'statistics_result.csv', frame_to_keyword)
    csv_io.write_csv(OUTPUT_ROOT_PATH + 'keyword_list.csv', [keyword_list])


def read_subtitle_file(subtitle_file):

    with open(subtitle_file, 'r') as subtitle:
        subtitle = subtitle.readlines()
    return subtitle


def keyword_matching(relation_patterns, line, subtitle_time, time_to_keyword, keyword_list):

    for relation in relation_patterns:
        if re.search(relation_patterns[relation], line.lower()):
            time_to_keyword.append([subtitle_time, relation])
            if relation not in keyword_list:
               keyword_list.append(relation) 
                
    return time_to_keyword, keyword_list

def to_frame_keyword(time_to_keyword): 

    frame_to_keyword = []
    for pair in time_to_keyword:
        start_frame, end_frame = time_format.to_frame(pair[0])
        new_pair = [start_frame, end_frame, pair[1]]
        frame_to_keyword.append(new_pair)

    return frame_to_keyword

if __name__=='__main__':
    if len(sys.argv) == 3:
        keyword_statistics(sys.argv[1], sys.argv[2])
    else:
        keyword_statistics('input/relationship.csv', 'input/movie.srt')
