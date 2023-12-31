"""
Sort a list of elements in ascending order

Compairs a list of elements pairwise and swaps the elements if element A is greater than 
element B and element A is at a lower index than element B. The greater elements travel to 
the higher indexes of the list and the comparisons are repeated on a decreasing length of the
list until all elements have been compared and have reached their final place in the list. 
"""

def bubble_sort(arr):
    n = len(arr) # variable eqaual to the number of elements in the list
    for i in range(n): # for loop going from 0 to n-1 (the index of the last element of the list)
        for j in range(0, n - i - 1): # for loop going from 0 to the index of the second to last element in the list
            if arr[j] > arr[j + 1]: # if the current element at index j is greater than the element after it at index j+1
                arr[j], arr[j + 1] = arr[j + 1], arr[j] # the current element and the element after it swap places in the list

