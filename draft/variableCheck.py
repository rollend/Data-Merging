# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 21:51:26 2018

@author: ROLLE
"""

def tccCheck(d1, d2):
        #Using set to check whether two dictionaries are match on Title, Country, City, regardless Score
        shared_items = set(d1.items()) & set(d2 .items())  
        country_check = False
        title_check = False
        city_check = False
        for e in shared_items:
            if 'country' in e:
                country_check = True
            if 'title' in e:
                title_check = True
            if 'city' in e:
                city_check = True
        if (country_check and title_check and city_check):
            return True
        else:
            return False
def cateCheck(d1, d2):
    shared_items = set(d1.items()) & set(d2 .items())  
    category_check = False    
    score_check = False
    for e in shared_items:
        if 'category' in e:
            category_check = True
        if 'score' in e:
            score_check = True        
    if (category_check and score_check):
        return True
    else:
        return False