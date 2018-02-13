# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 20:13:28 2018

Linear Search

@author: shen.xu
"""

import json
import re
import sys 

class Data_merge(object):
    def __init__(self, filename):
        self.gen = self.linear_search(filename)
        self.length = self.file_len(filename)
        self.filename = filename
        self.seen = set()

    def __len__(self):        
        return self.length

    def __iter__(self):        
        return self.gen
    
    def linear_search(self,filename):                
        with open(filename, 'r') as f:
            while True:                
                try:
                    for line in f:
                        title, category, city, country, score = self.extract_inf_from_string(line)                            
                        whole_pattern = '\"{}\": {{\"category\": {{\"\w*\": \d*}},\"country\": \"{}\", \"city\": \"{}\"'.format(title,country,city)                                                
                        if line not in self.seen:
                            add = True                                                        
                            if self.seen:                               
                                for each in self.seen:                                    
                                    if re.search(whole_pattern, each):
                                         title_seen, category_seen, city_seen, country_seen, score_seen = self.extract_inf_from_string(each)   
                                         if (int(score) > int(score_seen)):
                                             self.seen.remove(each)
                                             self.seen.add(line.strip('\n'))                                             
                                             add=False
                                         else:
                                             add=False                                                   
                                if add:
                                    self.seen.add(line.strip('\n'))                                    
                                else:
                                    continue
                            if not self.seen:
                                self.seen.add(line.strip('\n'))
                    for each in self.seen:
                        yield json.loads(each)
                    return
                except json.JSONDecodeError as e:
                    print(e)
                    continue

    def file_len(self,filename):
        with open(filename) as f:   
            for i, l in enumerate(f):
                pass
        return i + 1

    def extract_inf_from_string(self, line):        
        category_pattern = r'{"category": {"\w*": \d*}'
        country_pattern = r'"country": "([\w ]+)"'
        city_pattern = r'"city": ".*"'
        category_score_pattern = r'\d+'
        
        title = re.sub(category_pattern, '', line)                                      
        title = re.sub(country_pattern, '', title)
        title = re.sub(city_pattern, '', title)
        title = re.sub("[^\w]",' ',title).strip()
        
        try:
            country_string = re.search(country_pattern, line).group(0)
            country = re.sub('"country":', '', country_string)
            country = re.sub("[^\w]",' ',country).strip()
        except AttributeError as e:
            country = ""
            print(e)
            print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        
        try:
            city_string = re.search(city_pattern, line).group(0)
            city = re.sub('"city":', '', city_string)
            city = re.sub("[^\w]",' ',city).strip()
        except AttributeError as e:
            city = ""            
            
        category_string = re.search(category_pattern, line).group(0)
        category_score_string = re.sub('"category":', '', category_string)
        category = re.sub("\d*", '', category_score_string)
        category = re.sub("[^\w]",' ',category).strip()
        
        score = re.findall(category_score_pattern, category_score_string)
        if (len(score) == 1):
            score = score[0]        
        
        return title, category, city, country, score

    def find_unqiue_key(self, _list):    
        unique_key = []
        key_seen=set()
        for i in _list:
            for k in i.keys():
                key = str(k)
            if key not in key_seen:
                unique_key.append(key)
                key_seen.add(key)            
        return unique_key

if __name__ == '__main__':      
    
    h = Data_merge("merging_challenge_data.json")
    print(len(h))
    test = list(h.gen)
    testttt=list(h.seen)   
    print(testttt)

    
   
    