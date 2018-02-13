# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 10:13:28 2018

@author: shen.xu
"""

import json
import re
import itertools
from itertools import groupby
import operator
import sys
import time
import psutil
import os
from functools import wraps
from types import FunctionType
from memory_profiler import profile
import memory_profiler
import threading

"""
class MetaClass(type):
    def __new__(meta, classname, bases, classDict):
        newClassDict = {}
        for attributeName, attribute in classDict.items():
            if isinstance(attribute, FunctionType):
                # replace it with a wrapped version
                attribute = fn_timer(attribute)
            newClassDict[attributeName] = attribute
        return type.__new__(meta, classname, bases, newClassDict)

class JSON_Objects(MetaClass("NewBaseClass", (object,), {})):    
 """

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay) 
 
class JSON_Objects(object):    
    class Helper(object):
        @classmethod
        def fn_timer(self, function):   
         @wraps(function)
         def function_timer(*args, **kwargs):
             t0 = time.time()
             result = function(*args, **kwargs)
             t1 = time.time()
             print ("Total time running %s: %s seconds" %
                    (function.__name__, t1-t0)
                    )
             with open("Logging.txt", "a") as file:                                      
                 file.write("Total time running %s: %s seconds" %
                    (function.__name__, t1-t0)+"\n")
        
             return result
         return function_timer
     
    def __init__(self, filename):
        self.clock_start = self.logging()        
        self.gen = self.gen()
        self.length = self.file_len(filename)
        self.filename = filename
        self.seen = []
        self.load = self.readJSON(filename)       

    def __len__(self):        
        return self.length

    def __iter__(self):        
        return self.gen
    
    def gen(self):
        for i in self.seen:
            yield i
    
           
    def logging(self):
        clock_start = time.strftime("%Y-%m-%d %H:%M")
        with open("Logging.txt", "a") as file:                                      
                 file.write("Running Start at time: {}".format(clock_start)+"\n")
        return
    
    fp=open('memory_profiler.log','a')
    @profile(precision=10, stream=fp)
    def readJSON(self, filename):                       
        ln = 0        
        start = time.time()        
        print(filename)        
        with open(filename, 'r') as f:
            while True:                                     
                try:
                    for line in f:                        
                        d = self.flattenJSON(line)
                        """
                        title, category, city, country, score = self.extract_inf_from_string(line)                        
                        d = {"title":title, "category":category, "city":city, "country":country, "score":score}                        
                        whole_pattern = '\"{}\": {{\"category\": {{\"\w*\": \d*}},\"country\": \"{}\", \"city\": \"{}\"'.format(title,country,city)                                           
                        """
                        add = True                        
                        ln = ln+1
                        progress = round(ln/self.length,2)
                        for finished in [0.1, 0.25, 0.5, 0.75, 1]:                            
                            if progress == finished:
                                self.update_progress(finished) 
                                print("Mergeing Successed Lines:{}".format(ln))                                                          
                        if self.seen:
                            self.seen = sorted(self.seen, key = lambda item:item["score"])
                            """
                            add = self.linearSearch(d)                          
                            """
                            add = self.binarySearch(self.seen, 0, len(self.seen)-1, d)
                        
                            if add:
                                self.seen.append(d)                                                                    
                            else:                                
                                continue
                        if not self.seen:
                            self.seen.append(d)                 
                    end = time.time()
                    print("Merging Time: {}".format(end-start))
                    with open("Logging.txt", "a") as file:                                      
                            file.write("File Name: {}, Total Lines: {}, Merging Time: {}".format(filename, ln, end-start)+"\n")
                    self.seen = sorted(self.seen, key = lambda item:item["score"])                    
                    return self.seen
                except json.JSONDecodeError as e:
                    print(e)
                    continue   
    
    def linearSearch(self, d):               
        for idx, item in enumerate(self.seen):
            itemMatch = self.variableCheck(d, item)           
                                  
            if itemMatch:                                           
                if (int(d['score']) > int(item['score'])):
                    self.seen[idx].update(d)                                                                                         
                    return False
                else:
                    return False        
        return True     
    
    def binarySearch(self, arr, l, r, x):
        # Check base case
        if r >= l:     
            mid = int(l + (r - l)/2)
     
            # If element is present at the middle itself
            dd = arr[mid]            
            
            if self.variableCheck(x,dd):
                if int(x['score']) > int(dd['score']):
                    self.seen[mid].update(x)
                else:
                    return False
                return False
             
            # If element is smaller than mid, then it 
            # can only be present in left subarray
            elif int(arr[mid]["score"]) > int(x["score"]):
                return self.binarySearch(arr, l, mid-1, x)
     
            # Else the element can only be present 
            # in right subarray
            else:
                return self.binarySearch(arr, mid+1, r, x)     
        else:
            # Element is not present in the array
            return True
       
    def variableCheck(self, d1, d2):
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
        
    def file_len(self,filename):
        with open(filename) as f:   
            for i, l in enumerate(f):
                pass
        return i + 1

    def flattenJSON(self, line):
        column = ['title', 'category', 'city', 'country', 'score']
        line_load = json.loads(line)
        for key, item in line_load.items():
            title = key
            for k, i in item.items():
                if k == 'category':
                    for k, i in i.items():
                        category = k
                        score = i
                if k == 'city':
                    city = item['city']
                if k == 'country':
                    country = item['country']      
        d = {"title":title, "category":category, "city":city, "country":country, "score":score}
        return d
    
    def extract_inf_from_string(self, line):        
        category_pattern = r'{"category": {"\w*": \d*}'
        country_pattern = r'"country": ".*",'
        city_pattern = r'"city": ".*"'
        category_score_pattern = r'\d+'
        
        title = re.sub(category_pattern, '', line)                                      
        title = re.sub(country_pattern, '', title)
        title = re.sub(city_pattern, '', title)
        title = re.sub('[",:{}]',' ',title).strip()
        
        try:
            country_string = re.search(country_pattern, line).group(0)
            country = re.sub('"country":', '', country_string)
            country = re.sub("[^\w]",' ',country).strip()
        except AttributeError as e:
            country = ""
            print("Country:{}".format(e))
            print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        
        try:
            city_string = re.search(city_pattern, line).group(0)
            city = re.sub('"city":', '', city_string)
            city = re.sub("[^\w]",' ',city).strip()
        except AttributeError as e:
            city = ""
            print("City:{}".format(e))
            print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))            
        
        category_string = re.search(category_pattern, line).group(0)
        category_score_string = re.sub('"category":', '', category_string)
        category = re.sub("\d*", '', category_score_string)
        category = re.sub("[^\w]",' ',category).strip()
        
        score = re.findall(category_score_pattern, category_score_string)
        if (len(score) == 1):
            score = score[0]
        
        whole_pattern = '"Airport A": {"category": {"\w*": \d*}, "country": "\w*", "city": "\w*"'
        
        return title, category, city, country, score


    def find_unqiue_key(_list):    
        unique_key = []
        key_seen=set()
        for i in _list:
            for k in i.keys():
                key = str(k)
            if key not in key_seen:
                unique_key.append(key)
                key_seen.add(key)            
        return unique_key
    
    
    @Helper.fn_timer
    def dump(self):             
        with open("test111.json", "w") as file:
            ln = 0            
            for i in self.gen:
                d = {}
                d[i["title"]] = {"category":{i["category"]: int(i["score"])}, "country":i["country"], "city":i["city"]}               
                line = json.dumps(d)                
                file.write(line.replace("\\\\", "\\")+"\n")
                ln = ln + 1
                
    def update_progress(self, progress):
        barLength = 10 # Modify this to change the length of the progress bar
        status = ""
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = "error: progress var must be float\r\n"
        if progress < 0:
            progress = 0
            status = "Halt...\r\n"
        if progress >= 1:
            progress = 1
            status = "Done..."
        block = int(round(barLength*progress))
        text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
        sys.stdout.write(text)
        sys.stdout.flush() 
        
if __name__ == '__main__':
    pid = os.getpid()
    py = psutil.Process(pid)
    cpu_start = psutil.cpu_times()
    
    start_memory = memory_profiler.memory_usage()    
    spinner = Spinner()
    spinner.start()
    h = JSON_Objects("test100.txt")        
    h.dump()
    spinner.stop()
    after_memory = memory_profiler.memory_usage()
    cpu_end = psutil.cpu_times()
    with open("Logging.txt", "a") as file:                                      
        file.write("Memory Usage: {}Mb".format(float(after_memory[0])-float(start_memory[0]))+"\n")
        file.write("CPU Start Usage: {}".format(cpu_start)+"\n")
        file.write("CPU End Usage: {}".format(cpu_end)+"\n")
                    
    