# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 10:13:28 2018

@author: shen.xu

Python Version 3.6

Pre acquisities: psutil, Memory_profiler for monitoring purpose, can be removed

                Threading, Spinner on another thread without interfering main module, can be removed by removing spinner
                
Some concerns: Profiling significant reduce performance, almost tripled the time. 
"""

import json
import sys
import time
import psutil
from functools import wraps
import memory_profiler
#from memory_profiler import profile
from SearchAlgorithms import SearchAlgorithm
from SortingAlgorithms import SortingAlgorithm
#from Spinner import Spinner
from variableCheck import tccCheck

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False
 
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
     
    def __init__(self, args):
        self.args = args
        self.sorting = ['Bubble', 'Insertion', 'Selection', 'Timsort' ]
        self.searching = ['LinearSearch', 'BinarySearch', 'TernarySearch']
        self.clock_start = self.logging()                   
        self.length = self.file_len(args['-i'])
        self.filename = args['-i']
        self.seen = self.readJSON(args['-i'])
        self.load = self.readJSON(args['-i'])
        
                    

    def __len__(self):        
        return self.length

    def __iter__(self):        
        return self.gen   
           
    def logging(self):
        clock_start = time.strftime("%Y-%m-%d %H:%M")
        with open("Logging.txt", "a") as file:
                 file.write("="*50+"\n")                                      
                 file.write("Running Start at time: {}".format(clock_start)+"\n")
                 file.write("Sorting Algorithm: {}; Searching Algorithm:{}".format(self.args['-sorting'], self.args['-searching'])+"\n")
        return
    
    #fp=open("memory_profiler.log", "w+")
    #@profile(precision=5, stream=fp)
    def readJSON(self, filename):                       
        ln = 0        
        start = time.time()        
        print(filename)        
        with open(filename, 'r') as f:
            while True:                                     
                try:
                    # For scaling up, read line by line from JSON file
                    for line in f:                        
                        # Nested Dictionary is not convenient for implementing algorithms, thus flatten it, flatted collumn has reference in the function
                        d = self.flattenJSON(line)
                        # Monitoring progress                        
                        ln = ln+1
                        progress = round(ln/self.length,2)                        
                        self.updateProgress(progress) 
                        print("Mergeing Successed Lines:{}".format(ln)) 
                        # Check whether list existing or not                                                          
                        
                            # Sorting list for Binary Search according to Title, if linear search no need for sorting
                            # Timsort
                            
                        for x in self.seen:
                            if(tccCheck(d, x)):
                                if int(d['score']) > int(x['score']):
                                    yield json.loads(d)
                                else:
                                    pass                    
                            else:
                                yield json.loads(d)                          
                        
                                      
                    #Monitoring Total Merging time
                    end = time.time()
                    print("Merging Time: {}".format(end-start))
                    with open("Logging.txt", "a") as file:                                      
                            file.write("File Name: {}, Total Lines: {}, Merging Time: {}".format(filename, ln, end-start)+"\n")
                    # Need to sort list again as new data may come in
                    
                    #self.seen = SortingAlgorithm.merge_sort(self.seen, 'title')
                    print(self.seen)
                    return 
                except json.JSONDecodeError as e:
                    #Catch JSON decode Error and do something else if there is error
                    print(e)
                    continue   
    
    
    
    def searchTarget(self, target):
        for case in switch(self.args['-searching']):
            if case('LinearSearch'):
                self.seen = SearchAlgorithm.linearSearch(0, len(self.seen)-1, self.seen, target)
                continue
            if case('BinarySearch'):
                self.seen = SearchAlgorithm.binarySearch(0, len(self.seen)-1, self.seen , target)
                continue
            if case('TernarySearch'):
                self.seen = SearchAlgorithm.recTernarySearch(0, len(self.seen)-1, self.seen, target)
                continue    
    
    def assertSorted(self):
        for case in switch(self.args['-sorting']):
            if case('Bubble'):
                self.seen = SortingAlgorithm.bubble_sort(self.seen, 'title')
                continue
            if case('Insertion'):
                self.seen = SortingAlgorithm.insertion_sort(self.seen, 'title')
                continue
            if case('Selection'):
                self.seen = SortingAlgorithm.selection_sort(self.seen, 'title')
                continue
            if case('Timsort'):
                self.seen = sorted(self.seen, key = lambda item:(item["title"], item["country"], item["city"], item["score"]))
                continue    
    
    def file_len(self,filename):
        #Give total file length
        with open(filename) as f:   
            for i, l in enumerate(f):
                pass
        return i + 1

    def flattenJSON(self, line):
        """
        # Flatten column for sorting and searching
        column = ['title', 'category', 'city', 'country', 'score']
        """
        #Implemented as specified logic in JSON file
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
    
    #Helper.fn_timer wrap provide total time of dumping function
    #@Helper.fn_timer
    def dump(self):             
        if self.args['-o']:
            with open("{}{}{}{}{}".format(self.args['-o'], "_", self.args['-sorting'],  "_", self.args['-searching']), "w") as file:            
                #Reorganize flatten dictionary
                ln = 0            
                for i in self.seen:
                    d = {}
                    d[i["title"]] = {"category":{i["category"]: int(i["score"])}, "country":i["country"], "city":i["city"]}               
                    line = json.dumps(d)
                    #JSON dumps escape backslashes, replace when write                
                    file.write(line.replace("\\\\", "\\")+"\n")
                    ln = ln + 1
                print("Total Dumping Lines:{}".format(ln))
                with open("Logging.txt", "a") as file:
                    file.write("Total Dumping Lines:{}{}".format(ln, "\n"))
        else:
            print("No output file name! Using Test.txt instead!!!")
            with open("Result.txt", "w") as file:            
                #Reorganize flatten dictionary
                ln = 0            
                for i in self.seen:
                    d = {}
                    d[i["title"]] = {"category":{i["category"]: int(i["score"])}, "country":i["country"], "city":i["city"]}               
                    line = json.dumps(d)
                    #JSON dumps escape backslashes, replace when write                
                    file.write(line.replace("\\\\", "\\")+"\n")
                    ln = ln + 1
                print("Total Dumping Lines:{}".format(ln))
                with open("Logging.txt", "a") as file:
                    file.write("Total Dumping Lines:{}{}".format(ln, "\n"))
            
    def updateProgress(self, progress):
        #Update progress on console
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

def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0] == '-h':
            print("Usage of Command Line: -i input -o output (optional: -s second read file)")    
        elif argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

def dump(object):             
        if object.args['-o']:
            with open("{}{}{}{}{}".format(object.args['-o'], "_", object.args['-sorting'],  "_", object.args['-searching']), "w") as file:            
                #Reorganize flatten dictionary
                ln = 0            
                for i in object.seen:
                    d = {}
                    d[i["title"]] = {"category":{i["category"]: int(i["score"])}, "country":i["country"], "city":i["city"]}               
                    line = json.dumps(d)
                    #JSON dumps escape backslashes, replace when write                
                    file.write(line.replace("\\\\", "\\")+"\n")
                    ln = ln + 1
                print("Total Dumping Lines:{}".format(ln))
                with open("Logging.txt", "a") as file:
                    file.write("Total Dumping Lines:{}{}".format(ln, "\n"))
        else:
            print("No output file name! Using Test.txt instead!!!")
            with open("Result.txt", "w") as file:            
                #Reorganize flatten dictionary
                ln = 0            
                for i in object.seen:
                    d = {}
                    d[i["title"]] = {"category":{i["category"]: int(i["score"])}, "country":i["country"], "city":i["city"]}               
                    line = json.dumps(d)
                    #JSON dumps escape backslashes, replace when write                
                    file.write(line.replace("\\\\", "\\")+"\n")
                    ln = ln + 1
                print("Total Dumping Lines:{}".format(ln))
                with open("Logging.txt", "a") as file:
                    file.write("Total Dumping Lines:{}{}".format(ln, "\n"))

def streaming(myargs):
    cpu_start = psutil.cpu_times() #Monitoring CPU times    
    start_memory = memory_profiler.memory_usage()    #Monitoring Memory at start           
    try:
        if myargs['-s']:
            h = JSON_Objects(myargs)       
            h.readJSON(myargs['-s'])
            h.dump()
    except KeyError as e:
        h = JSON_Objects(myargs)
        print(h.seen)
        dump(h)
    after_memory = memory_profiler.memory_usage() #Get Memory usage after program
    cpu_end = psutil.cpu_times() #Monitoring CPU times
                
                #Write monitoring information to file
    with open("Logging.txt", "a") as file:                                      
        file.write("Memory Usage: {}Mb".format(float(after_memory[0])-float(start_memory[0]))+"\n")
        file.write("CPU Start Usage: {}".format(cpu_start)+"\n")
        file.write("CPU End Usage: {}".format(cpu_end)+"\n")
        
if __name__ == '__main__':
    
    myargs = getopts(sys.argv)
    
    """
    spinner = Spinner() #Start spinner
    spinner.start()
    """
    Implemented_Sorting_Algorithms = ['Timsort']
    Implemented_Searching_Algorithms = ['BinarySearch', 'TernarySearch', 'LinearSearch']
    
    try:
        if myargs['-sorting']:
            if myargs['-searching']:            
                streaming(myargs)       
    except KeyError as e:
        for each in Implemented_Sorting_Algorithms:
            myargs['-sorting'] = each        
            for alg in Implemented_Searching_Algorithms:                
                myargs['-searching'] = alg    
                streaming(myargs)
            
    """
    spinner.stop() # Stop Spinner
    """
    
                    
    #Job done