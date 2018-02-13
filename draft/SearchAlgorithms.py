# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 21:38:25 2018

@author: ROLLE
"""

from variableCheck import tccCheck

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
        if right >= left:     
            mid = int(left + (right - left)/2)
            midpoint = A[mid]["title"]
            # If element is present at the middle itself 
            if midpoint == target['title']:                
                if tccCheck(target, A[mid]):
                    if int(target['score']) > int(A[mid]['score']):
                        A[mid].update(target)
                    else:
                       pass
                    return A
                A.append(target)
                return A                  
                 
                # If element is smaller than mid, then it 
                # can only be present in left subarray
            elif (midpoint > target["title"]):
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
            
            oneThirdpoint = A[oneThird]['title']
            twoThirdpoint = A[twoThird]['title']
    
            if(oneThirdpoint == target['title']):
                if(tccCheck(target, A[int(oneThird)])):
                    if int(target['score']) > int(A[oneThird]['score']):
                        A[int(oneThird)].update(target)
                    else:
                        pass
                    return A
                A.append(target)
                return A
            elif(twoThirdpoint == target['title']):
                if(tccCheck(target, A[int(twoThird)])):
                    if int(target['score']) > int(A[int(twoThird)]['score']):
                        A[int(twoThird)].update(target)
                    else:
                        pass
                    return A
                A.append(target)
                return A
            
            elif(target['title'] < oneThirdpoint):
                return SearchAlgorithm.recTernarySearch(left, oneThird-1, A, target)
            elif(twoThirdpoint < target['title']):
                return SearchAlgorithm.recTernarySearch(twoThird+1, right, A, target)
            
            else:
                return SearchAlgorithm.recTernarySearch(oneThird+1, twoThird-1, A, target)
        else:            
            A.append(target)
            return A  
        
        
        