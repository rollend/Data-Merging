# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 17:07:16 2018

@author: ROLLE
"""
from heapq import merge

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
       
   
    