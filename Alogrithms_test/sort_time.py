import pandas as pd
import bubble_sort
import merge_sort
from timeit import repeat
from typing import Callable
import book_data



titles10k=book_data.get_book_titles_from_csv("10kbooks.csv")
titles1000=titles10k[:1000]
titles100=titles10k[:100]
titles10=titles10k[:10]

all_titles=[titles10, titles100, titles1000, titles10k]

algorithms=["bubble_sort", "merge_sort"]

"""
Measure the execution time of a given algorithm with a given dataset

Uses the timeit module's repeat function which needs the location of the algorithm
used and the statement that it needs to execute. In this function, the statement
is executed 5 times and the whole process is repeated 3 times. The function returns
the times of the 3 tests in a list. Based on code from realpython.com
"""
def time_sort_test(algorithm: str, dataset: list) -> list:
    setup_code=f"from {algorithm} import {algorithm}"
    statement=f"{algorithm}({dataset})"
    times=repeat(setup=setup_code, stmt=statement, repeat=3, number=5)

    return times

times=time_sort_test("bubble_sort", titles100)

results=[]

for algo in algorithms:
    for dataset in all_titles:
        time=min(time_sort_test(algo, dataset))
        results.append(f"{algo} took {time} to sort {len(dataset)} elements")

res_str="/n".join(results)
print(res_str)



