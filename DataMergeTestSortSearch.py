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
#import memory_profiler
import os
#from memory_profiler import profile
#from Spinner import Spinner

class SortingAlgorithm():
    
    def bubble_sort(lst, variable):
        changed = True
        while changed:
            changed = False
            for i in range(len(lst) - 1):
                if lst[i][variable] > lst[i+1][variable]:
                    lst[i], lst[i+1] = lst[i+1], lst[i]
                    changed = True
        return lst
    
    def insertion_sort(lst, variable):
        for i in range(1, len(lst)):
            j = i-1
            key = lst[i][variable]
            item = lst[i]
            while (lst[j][variable] > key) and (j >= 0):
               lst[j+1] = lst[j]
               j -= 1
            lst[j+1] = item
        return lst
            
    def selection_sort(lst, variable):
        for i in range(len(lst)):
            for j in range(i, len(lst)):
                if(lst[i][variable] > lst[j][variable]):
                    lst[i], lst[j] = lst[j], lst[i]
        return lst   
    
    #Maximum recursion depth exceeded in comparison when line 1000
    def quicksort(lst, variable):
        if len(lst) == 1 or len(lst) == 0:
            return lst
        else:
            pivot = lst[0][variable]
            i = 0
            for j in range(len(lst)-1):
                if lst[j+1][variable] < pivot:
                    lst[j+1],lst[i+1] = lst[i+1], lst[j+1]
                    i += 1
            lst[0],lst[i] = lst[i],lst[0]
            first_part = SortingAlgorithm.quicksort(lst[:i],variable)
            second_part = SortingAlgorithm.quicksort(lst[i+1:],variable)
            first_part.append(lst[i])
            return first_part + second_part

class SearchAlgorithm():
    def linearSearch(left, right, A, target):
            for i in range(left, right+1):
                if(tccCheck(target, A[i])):
                    if int(target['score']) > int(A[i]['score']):
                        A[i].update(target)
                    else:
                        pass
                    return A
            A.append(target)
            return A    
    
    def binarySearch(left, right, A, target):        
        #Binary search has time complexity O(log n)    
        # Check base case
        precision = 10 
        if(right-left < precision):
                return SearchAlgorithm.linearSearch(left,right,A,target)
        if right >= left:     
            mid = int(left + (right - left)//2)
            midpoint = "{}".format(A[mid]["title"])
            # If element is present at the middle itself 
            targetpoint = "{}".format(target["title"])                
            if midpoint == targetpoint:
                for i in (A[mid-5:mid+5]):                    
                    if tccCheck(target, i):
                        if int(target['score']) > int(A[mid]['score']):
                            A[mid].update(target)
                        else:
                            pass
                        return A
                    else:
                        return A      
                 
                # If element is smaller than mid, then it 
                # can only be present in left subarray
            elif (midpoint > targetpoint):
                return SearchAlgorithm.binarySearch(left, mid-1, A, target)
         
                # Else the element can only be present 
                # in right subarray
            else:
                return SearchAlgorithm.binarySearch(mid+1, right, A, target)     
        else:
            # Element is not present in the array
            A.append(target)
            return A
    
    # This is the recursive method of the ternary search algorithm.
    def recTernarySearch(left, right, A, target):
        # This is the precision for this function which can be altered.
        # It is recommended for users to keep this number greater than or equal to 10.
        precision = 10        
        if(left<right):
        
            if(right-left < precision):
                return SearchAlgorithm.linearSearch(left,right,A,target)
    
            oneThird = int(left + (right - left)/3);
            twoThird = int(left + 2*(right - left)/3);
            
            oneThirdpoint = "{}".format(A[oneThird]["title"])
            twoThirdpoint =  "{}".format(A[twoThird]["title"])
            targetpoint = "{}".format(target["title"])
    
    
            if(oneThirdpoint == targetpoint):
                for i in (A[oneThird-5:oneThird+5]):
                    if(tccCheck(target, A[int(oneThird)])):
                        if int(target['score']) > int(A[oneThird]['score']):
                            A[int(oneThird)].update(target)
                        else:
                            pass
                        return A
                    else:
                        return A
            elif(twoThirdpoint == targetpoint):                
                for i in (A[twoThird-5:twoThird+5]):
                    if(tccCheck(target, A[int(twoThird)])):
                        if int(target['score']) > int(A[int(twoThird)]['score']):
                            A[int(twoThird)].update(target)
                        else:
                            pass
                        return A
                    else:
                        return A
            
            elif(targetpoint < oneThirdpoint):
                return SearchAlgorithm.recTernarySearch(left, oneThird-1, A, target)
            elif(twoThirdpoint < targetpoint):
                return SearchAlgorithm.recTernarySearch(twoThird+1, right, A, target)
            
            else:
                return SearchAlgorithm.recTernarySearch(oneThird+1, twoThird-1, A, target)
        else:            
            A.append(target)
            return A 

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
 
class streamingJSON(object):    
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
        self.seen = []
        self.load = self.readJSON(args['-i'])
        self.gen = self.gen()
                    

    def __len__(self):        
        return self.length

    def __iter__(self):        
        return self.gen
    
    def gen(self):
        for i in self.seen:
            yield i
        self.seen = []
        
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
                        if self.seen:
                            # Sorting list for Binary Search according to Title, if linear search no need for sorting
                            # Timsort
                            self.assertSorted()
                            self.searchTarget(d)                             
                        if not self.seen:
                            self.seen.append(d)                 
                    #Monitoring Total Merging time
                    end = time.time()
                    print("Merging Time: {}".format(end-start))
                    with open("Logging.txt", "a") as file:                                      
                            file.write("File Name: {}, Total Lines: {}, Merging Time: {}".format(filename, ln, end-start)+"\n")
                    # Need to sort list again as new data may come in
                    self.assertSorted()
                    #self.seen = SortingAlgorithm.merge_sort(self.seen, 'title')
                    return self.seen
                except json.JSONDecodeError as e:
                    #Catch JSON decode Error and do something else if there is error
                    print(e)
                    continue   
    
    def partition(self, targetList):
        left = 0 
        right = len(targetList)-1
        targetList[left:i]
        targetList[i+1:j]
        targetList[j+1:k]
        targetList[k+1:h]
        targetList[h+1:right]
        return
    
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
    @Helper.fn_timer
    def dump(self):             
        if self.args['-o']:
            with open("{}{}{}{}{}".format(self.args['-o'], "_", self.args['-sorting'],  "_", self.args['-searching']), "w") as file:            
                #Reorganize flatten dictionary
                ln = 0            
                for i in self.gen:
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
                for i in self.gen:
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
            print("Usage of Command Line: -i input -o output (optional: -s second read file) (optional: -sorting -searching) \n")
            print("You can specify algorithm. Or leave it empty then script will run through all algorithms! ")
        elif argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

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

def streaming(myargs):
    process = psutil.Process(os.getpid())    
    cpu_start = psutil.cpu_times() #Monitoring CPU times    
    #start_memory = memory_profiler.memory_usage()    #Monitoring Memory at start           
    try:
        if myargs['-s']:
            h = streamingJSON(myargs)       
            h.readJSON(myargs['-s'])
            h.dump()
    except KeyError as e:
        h = streamingJSON(myargs)
        h.dump()
    #after_memory = memory_profiler.memory_usage() #Get Memory usage after program
    cpu_end = psutil.cpu_times() #Monitoring CPU times
                
                #Write monitoring information to file
    with open("Logging.txt", "a") as file:                                      
        #file.write("Memory Usage: {}Mb".format(float(after_memory[0])-float(start_memory[0]))+"\n")
        file.write("Memory Usage: {}MB{}".format(float(process.memory_info().rss)/1048576, "\n"))
        file.write("CPU Start Usage: {}{}".format(cpu_start,"\n"))
        file.write("CPU End Usage: {}{}".format(cpu_end,"\n"))
        
if __name__ == '__main__':
    
    myargs = getopts(sys.argv)
    
    """
    spinner = Spinner() #Start spinner
    spinner.start()
    """
    Implemented_Sorting_Algorithms = ['Timsort']
    Implemented_Searching_Algorithms = ['BinarySearch', 'TernarySearch']
    
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