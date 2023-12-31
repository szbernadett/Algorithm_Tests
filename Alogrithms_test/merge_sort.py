"""
Sort a list of elements in ascending order 

Takes a list of elements and creates list smaller and smaller list slices until it reaches
a slice with 2 elements, with the left and right slices containing one element each. 
Compares the elements and adds them to a list in sorted order. Recursively repeats the 
sorting and merging operations with bigger and bigger list slices until all elements of the
original list are in ascending order. 
"""

def merge_sort(arr):
    if len(arr) > 1:           # if the array contains more than one element
        mid = len(arr) // 2    # define the middle index of the array
        left_half = arr[:mid]  # create a slice from the first (inclusive) to the middle (exclusive) index
        right_half = arr[mid:] # create a slice from the middle to the final index

        merge_sort(left_half)  # recursive calls to merge_sort resulting in
        merge_sort(right_half) # the function being called until the list slices reach an element count of 2

        merge(arr, left_half, right_half) # when the list slices reach an element count of 2, the mid index will be 1, the left half will contain element at index 0
                                          # the right half will contain the element at index 1 and the first two elements will be sorted and merged by calling the merge function


def merge(arr, left, right): 
    i = j = k = 0 # i = index of left half, j = index of right half, k = index of merged array

    while i < len(left) and j < len(right): # compare i and j to the lengths of the left and right half list slices to avoid IndexError
        if left[i] < right[j]:              # if the element at index i of the left slice is smaller than the element at index j of the right slice 
            arr[k] = left[i]                # the smaller element will be at current index k in the merged list
            i += 1                          # increment current index of left half
        else:
            arr[k] = right[j] # if element at index j in the right half is the smaller one, let that be at index k in the merged list
            j += 1            # increment current index of right half
        k += 1                # increment current index of merged array

    while i < len(left): # if the current index of the left list slice is still smaller than the length of the left slice 
        arr[k] = left[i] # the element at the current index i of the left slice will be at current index k of the merged list
        i += 1           # increment current index of left list slice
        k += 1           # increment current index of merged list

    while j < len(right): # if the current index of the right list slice is still smaller than the length of the right slice
        arr[k] = right[j] # the element at the currend index j of the right slice will be at current index k of the merged list
        j += 1            # increment current index of right half
        k += 1            # increment current index of merged array


