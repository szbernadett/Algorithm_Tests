from __future__ import annotations
import pandas as pd
import new_search_util
import presenter
from constants import *

"""
Create a nested dictionary that uses the ISBN numbers
as keys to each book

Creates a pandas dataframe from a given csv file (path).
Iterates over each row of the dataframe and for each
row,creates an inner dictionary that is populated with
all book information except the ISBN. The ISBN numbers are
used as keys to the inner dictionaries.

The underscore in the for loop is used to indicate that the 
index value of the (index, Series) pair that iterrows() returns
is intentionally ignored

"""
def create_books_from_csv(path: str):
    contents = pd.read_csv(path)
    contents["Year"]=contents["Year"].astype("Int64")
    contents.dropna(inplace=True)
    books = {}
    for _, row in contents.iterrows():
        isbn = row['ISBN']
        book_details = {
            "Title": row["Title"],
            "Author": row["Author"],
            "Publisher": row["Publisher"],
            "Year": str(row["Year"])
        }
        books[isbn] = book_details

    return books

books=create_books_from_csv(BookData.THOUSAND)



"""
Extract book titles from csv to Python list

Access a csv file withen given path and extract all data from
the Title column to a pandas dataframe, then convert dataframe
to Python list
"""
def get_book_titles_from_csv(csv_path: str) -> list:
    dataframe=pd.read_csv(csv_path)
    dataframe=dataframe[["Title"]]
    titles=dataframe["Title"].tolist()

    return titles


"""
Add words and year from book info to index mapped to ISBNs

Populates the index dictionary with the title, author and publisher
info. Gathers all information split into words into a list. Then 
determines whether the word already exists in the index as a key, 
and if not, adds it as a new key along with an empty set as a value.
This happens by calling the setdefault method on the index, which either
returns the existing set of ISBNs or adds the new key - value pair as 
described above. The year information of the book is added with the 
same method.
"""
def add_book(search_index: dict[str, set[str]], isbn: str, book: dict[str, str], keyword: str) -> None:
    words=new_search_util.prepare_string(book[keyword]) if keyword == "Title" or "Author" or "Publisher" else None
    if words is not None:
        for word in words:
         search_index.setdefault(word, set()).add(isbn)
    else:
        search_index.setdefault(book[keyword], set()).add(isbn) # add the year info


# Create a data structure for the book info fields
title_author_publisher_index={}
year_index={}
isbn_list=list(books.keys())

# Populate indices 
for isbn, book in books.items():
    add_book( title_author_publisher_index, isbn, book, "Title")
    add_book(title_author_publisher_index, isbn, book, "Author")
    add_book(title_author_publisher_index, isbn, book, "Publisher")
    add_book(year_index, isbn, book, "Year")
