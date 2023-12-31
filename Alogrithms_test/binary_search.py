from constants import *
"""
Simple binary search

Find a string or an int in a sorted list of strings
or integers (source). Determine the start and end
of the searched area within a list, find the midpoint
and compare the target string or int to the element
in the midpoint. If a match was found, return the result.MACHT_FOUND.
If the target element is smaller that the midpoint element,
recursively call binary_search with a slice of the source
list that starts at index 0 and ends at midpoint - 1. 
If the target is greater than the midpoint element, 
recursively call binary_search with a slice of the list that
starts and the midpoint index and ends at the last index of 
the current list. The algorithms runs until it the target
element is found or the element was not found but the source
cannot be sliced further.
"""
def binary_search(source: list, target: str|int) -> int:
    if type(target) != int and type(target) != str:
        return Result.NOT_FOUND 
    
    start, end = 0, len(source)-1 # start and end is always at the beginning and the end
                                  # of the list because the list is sliced (into shorter and
                                  # shorter lists) with each recursive call
    
    if end < 0:
        return Result.NOT_FOUND

    mid = start + end // 2
    comparand=source[mid] 

    try:
        if target == comparand:
            return Result.MATCH_FOUND

        if target < comparand:
            return binary_search(source[0:mid], target)

        if target > comparand:
            return binary_search(source[mid+1:], target)
    except:
        return Result.NOT_FOUND

"""
Find the index of the word that is the first to match a given length in
a sorted list of strings

The algorithm works similarly to simple binary search up to the point
where it finds the first element that matches the target lenght. Then
it determindes whether that is the first occuurrence of that word length
and if not, continues to recursively search for the first occurrence.
"""


def binary_search_by_string_length(source: list, target_length: int, start=0, end=None) -> int:
    if not source or type(target_length) != int:
        return Result.NOT_FOUND
    
    if end is None:
        end=len(source)-1
        if target_length < len(source[0]) \
        or target_length > len(source[end])\
        or type(target_length) is not int:
            return Result.NOT_FOUND

    if start > end:
        return Result.NOT_FOUND

    mid=(start + end) // 2
    comparand_length=len(source[mid])

    if comparand_length == target_length:
        if mid==0 or len(source[mid-1]) < comparand_length:
            return mid
        else:
            return binary_search_by_string_length(source, target_length, start, mid-1)
        
    if target_length < comparand_length:
        return binary_search_by_string_length(source, target_length, 0, mid-1)
    
    if target_length > comparand_length:
        return binary_search_by_string_length(source, target_length, mid+1, end)
    

