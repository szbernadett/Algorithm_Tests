from __future__ import annotations
import re
from itertools import combinations
import nltk
from nltk.corpus import stopwords
from levenshtein_distance import *
import binary_search
from presenter import Presenter
from constants import *
from typing import Callable

################################################################################################
#                                            PREPARE                                           #
#                                          SEARCH TERMS                                        #
################################################################################################

nltk.download("stopwords")
stop_words=set(stopwords.words("english"))
stop_words_es=set(stopwords.words("spanish"))
stop_words_de=set(stopwords.words("german"))
stop_words_fr=set(stopwords.words("french"))
stop_words.update(stop_words_es)
stop_words.update(stop_words_de)
stop_words.update(stop_words_fr)

"""
ISBN regex from https://www.oreilly.com/library/view/regular-expressions-cookbook/9780596802837/ch04s13.html
"""
isbn_regex="^(?:ISBN(?:-1[03])?:? )?(?=[-0-9 ]{17}$|[-0-9X ]{13}$|[0-9X]{10}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?(?:[0-9]+[- ]?){2}[0-9X]$"
isbn_pattern=re.compile(isbn_regex)

"""
Keep only alphanumberic characters in a string. Replace unwanted
(special) characters with empty string. Leave whitespace.
"""
def remove_special_characters(string_to_clean)-> str:
    alphanum_pattern = r'[^A-Za-z0-9 ]+'
    cleaned_string = re.sub(alphanum_pattern, "", string_to_clean)
    
    return cleaned_string

"""
Return text split into list of words

Punctuation, special characters, trailing and leading whitespace 
and stop words are removed and text is transformed to lowercase then split into words.
"""
def prepare_string(text: str) -> list[str]:
    text=text.strip()
    text=remove_special_characters(text)
    words=text.lower().split()
    filtered_words=[word[:Search.MAX_WORD_LENGTH] for word in words if word not in stop_words and len(word) > 1]
    return filtered_words

"""
Create a simple list from a list of sets

Create an new list, iterate over the list of sets
and create a list of each set, then extend the new 
list with the list created from the set, resulting
in the original list of sets to be "flattened" into
a simple list.
"""

################################################################################################
#                                     RESULT PROCESSING AND                                    #
#                                       RANKING FUNCTIONS                                      #
################################################################################################

def unpack_list_of_sets(list_to_unpack: list[set]) -> list:
    elements=[]
    if not list_to_unpack:
        return elements
    for set_in_list in list_to_unpack:
        list_to_add=[x for x in set_in_list]
        elements.extend(list_to_add)
    return elements

"""
Find all elements in a group of sets that are in any of the
intersections of the group, except the intersection of all groups

Create all possible combinations of a group of sets with a given
grouping size (2,3,4 etc.). In each group of sets, find all the
elements that are in the intersections of these sets and deduct
the elements that are in the mutual intersection of all sets 
(non_unique_elements) - this is to avoid repeating these elements 
several times. 
Example: in a list of four sets where the sets are A, B, C, D, group 
the sets in pairs and find the elements in their intersection. The pairs 
will be AB, AC, AD, BC, BD, and CD. When finding the elements in the 
intersection of these set pairs, the elements that are in the intersection 
of ABCD would be repeated 6 times, which is why they are removed. The same 
logic is used for groups of 3, 4 etc. sets.  
"""
def elements_in_intersections(list_of_sets: list[set], grouping_size: int, non_unique_elements: set) -> list[set]:
    elements=[]
    if not list_of_sets or grouping_size < 2:
        return elements
    set_groups=combinations(list_of_sets, grouping_size)
    for set_group in set_groups:
        elements.append(set.intersection(*set_group)-non_unique_elements)
        elements=[x for x in elements if x] # remove empty sets
    return elements

"""
Find all elements in all possible intersections of a list of sets

Create a list that contains all elements in a list of sets that are repeated
in more than one set, in other words that are in the intersection of two or
more sets. Sets are examined in groups, where the size of the groups starts
from the number of sets - 1 to 2 (so for a list of 5 sets, from 4 to 2). The
intersection of all groups in the list is treated separately to avoid repetition
of the elements in that intersection. The elements are added in descending
order depending on how many intersections they appeared in, so the ones
that are in the intersection of all sets are added first, then the ones that
appear in the intersection  of len(list_of_sets)-1 number of sets etc. with the
ones appearing in the intersection of two sets being added last. 
"""
def find_all_elements_in_intersections(list_of_sets: list[set]) -> list[set]:
    all_intersection_elements=[]
    if not list_of_sets:
        return all_intersection_elements
    intersection_of_all_sets=set.intersection(*list_of_sets)
    all_intersection_elements.append(intersection_of_all_sets)
    grouping_size=len(list_of_sets)-1
    while grouping_size >= 2:
        all_intersection_elements.extend(elements_in_intersections(list_of_sets, grouping_size, intersection_of_all_sets))
        grouping_size -= 1
    all_intersection_elements=[x for x in all_intersection_elements if x]
    return all_intersection_elements

"""
Find all elements that are not in an intersection 

Takes the union of all sets in a list and removes the elements that are in the
intersection of any number of the sets.
"""

def find_all_set_differences(list_of_sets: list[set], all_elements_in_intersections: list) -> set[str]:
    diffs = []
    if not list_of_sets:
        return diffs
    differences=set.union(*list_of_sets)
    differences.difference_update(all_elements_in_intersections)
    diffs=list(differences)
    return diffs

"""
Create a list that contains the result ISBNs in descending order of relevance

The order of relevance is defined how many sets the ISBN appears in, 
where a list of sets represents the result of a word-based search.
Each matched word relates to a set in the search_index (dictionary)  
that contains one or more ISBN, and that set is then added to a list.
When the search is finished, the number of times each ISBN appears
in the sets within the result list is examined by determining
if it appers in any of the intersections of the sets in the list.
If it appears in the intersection of all sets, that will be the 
most relevant search result and added first to the list within
the rank_results function. Next is any ISBN that appears in
the intersection of at least two, but not all sets, and finally
those that only appear in one set. In case all sets are disjoint,
all search results will be considered of equal relevance. 

"""
def rank_results(results: list[set]) -> list[str|int]:
    ranked_results=[]
    if not results:
        return ranked_results
    all_elements_in_intersections=unpack_list_of_sets(find_all_elements_in_intersections(results))
    ranked_results.extend(all_elements_in_intersections)
    ranked_results.extend(find_all_set_differences(results, all_elements_in_intersections))
    return ranked_results

"""
Return ISBNs of matching books in ascending order of edit distance and occurrence

Gets the ISBN numbers corresponding to the matched words in the result dictionary. 
The ISBNs are retrieved from the search_index in the form of a list of sets. The 
list of sets are then passed to a function that ranks the ISBN numbers according 
to how many times they appear, using the relationship (intersection and difference) 
between the sets. The ranked list of ISBNS are the added to the final list where
the most relevant results will be at the front of the list. The most relevant results
will be the ISBNs that corresponded to words with the lowest edit distance to the 
search term and possibly appeared more than once in the results list. For example, 
if the search term was 'Harry Potter', the most relevant result (ISBN) would be the 
one that includes both words with 0 edit distance, followed by results that match 
either 'Harry' or 'Potter' with 0 edit distance but not both, or match one with 0 
edit distance and the other with 1 or 2 edit distance and so on, until the results 
only contain a match for one of the words with an edit distance of 2. 
"""

def order_results(results: dict[int, str], search_index: dict[str, set[str]]) -> list[str]:
    ordered_results=[]
    if not results or not search_index:
        return ordered_results
    edit_distances=list(results.keys())
    if 0 in edit_distances:
        dist0=[search_index[res] for res in results[0]]
        ranked0=rank_results(dist0)
        ordered_results.extend(ranked0)
    if 1 in edit_distances:
        dist1=[search_index[res] for res in results[1]]
        ordered_results.extend(unpack_list_of_sets(dist1))
    if 2 in edit_distances:
        dist2=[search_index[res] for res in results[2]]
        ordered_results.extend(unpack_list_of_sets(dist2))
    
    return ordered_results


################################################################################################
#                                          WORD SEARCH                                         #
#                                         'IN' OPERATOR                                        #
################################################################################################

"""
Return list of ISBN numbers of books whose info
matches or contains the search term using the "in" operator


Book info consisting of author, title, publisher and year is scanned for match
with the search term, which is by default one word or a string of characters.
A search term matches a word if it is the same length or shorter
than the word and is either a substring of the word or consists of the same characters
in the same order as the word. The search index is the dictionary containing title, publisher
and author info as keys and sets of ISBNS as values. The source list is the list created from
the keys of the search index, sorted by string length. The source list is sliced based on the
length of the search term - words shorter than the search term are omitted as they would not
result in a match. 
"""
def search_single_match(search_index: dict[str, set[str]], search_source:list[str], term_to_find: str, presenter: Presenter, search_info_key: tuple[tuple[str], SearchType]) -> list[set]:
    matched_words=[]
    result_sets=[]
    if not search_index or not term_to_find or type(term_to_find) != str or not search_source or not presenter or not search_info_key:
        return result_sets
    start_index=binary_search.binary_search_by_string_length(search_source, len(term_to_find))
    if start_index > 0 :
        search_source_slice=search_source[start_index:]
    else:
        search_source_slice=search_source
    matched_words=[word for word in search_source_slice if term_to_find in word] # add matching words from the index_words list if the 
                                                                         # search term matches the full length of the word of is a substring of the word
    presenter.search_info[search_info_key].setdefault(SearchInfo.MATCHED_STRINGS, list()).extend(matched_words)
    result_sets=[search_index[match] for match in matched_words] # results in a list of sets, which are values of the keys (matched words) of the 
                                                                         # inverted_index and contain the ISBNs of the matched books
    return result_sets

"""
Repeatdly run the search_single_match function to search
for each search term, if the search term was an expression
that consists of multiple words
"""

def search_multiple_matches(search_index: dict[str, set[str]], search_source: list[str], terms_to_find: list, presenter: Presenter, search_info_key: tuple[tuple[str], SearchType]) -> list[set]:
    results=[]
    if not search_index or not terms_to_find:
        return results
    for term in terms_to_find:
        results.extend(search_single_match(search_index, search_source, term, presenter, search_info_key))
    return results


################################################################################################
#                                          WORD SEARCH                                         #
#                                     LEVENSHTEIN DISTANCE                                     #
################################################################################################

def slice_list_for_levenshtein_search(source: list[str], target_length: int) -> list[str]:
    if not source or type(target_length) != int:
        return source
    lower_target=0
    upper_target=0
    if target_length - Search.LEVENSHTEIN_MAX_DISTANCE < len(source[0]):
        lower_target=target_length
    else:
        lower_target=target_length - Search.LEVENSHTEIN_MAX_DISTANCE
    if target_length + Search.LEVENSHTEIN_MAX_DISTANCE > len(source[len(source)-1]):
        upper_target=target_length
    else:
        upper_target=target_length + Search.LEVENSHTEIN_MAX_DISTANCE + 1
    slice_start=binary_search.binary_search_by_string_length(source, lower_target)
    slice_end=binary_search.binary_search_by_string_length(source, upper_target)

    if slice_start != -1 and slice_end != -1:
        source_slice=source[slice_start:slice_end]
    elif slice_start != -1:
        source_slice=source[slice_start:]
    elif slice_end != -1:
        source_slice=source[:slice_end]
    else:
        source_slice=source

    return source_slice

"""
Return list of words that match search term(s) based on their Levenshtein distance

The maximum allowed distance in this case is 2, given that even
and edit distance of 1 can mean a significant difference, however
typing mistakes can still easily create a larger edit distance with
the word remaining recognisably similar to its properly typed form. 
The source list is sliced based on the length of the search term(s) and
the maximum allowed Levenshtein distance, resulting in a list with words
ranging from 2 characters shorter to 2 characters longer in length than
the search term. 
Matching words are added to a dictionary, where the keys are integers 
representing the edit distance. The search stops after finding 100
results (defined as a constant).
"""
def search_by_levenshtein_distance(source: list[str], presenter: Presenter, search_info_key: tuple[tuple[str], SearchType]) -> dict[int, str]:   
    results={}
    if not source or not presenter or not search_info_key:
        return results    
    search_terms=search_info_key[0]
    for word in search_terms:
        source_slice=slice_list_for_levenshtein_search(source, len(word)) if len(word) > Search.LEVENSHTEIN_MAX_DISTANCE else source
        count=0
        for source_word in source_slice:
            if count > Search.MAX_RESULT_COUNT:
                break
            dist = levenshtein_distance(source_word, word)
            if dist < 3:
                results.setdefault(dist, list()).append(source_word)
                presenter.search_info[search_info_key].setdefault(SearchInfo.MATCHED_STRINGS, list()).append(source_word)
                count += 1
    return results





################################################################################################
#                         SEARCH AND RANK RESULTS ('IN' OR LEVENSHTEIN)                        #
#                           AND PASS TO PRESENTER TO APPEAR ON SCREEN                          #
################################################################################################

"""
Call the functions that find matches between search term and book info and
rank the results, return list with the info of all matching books

Prepare the search term by removing all unwanted characters and words. If 
the search term is only one word, search for a single match. If there are
more words, search for multiple matches. 
"""
def search_all_with_in_operator(search_index: dict[str, set[str]], search_source: list[str], presenter: Presenter, search_info_key: tuple[tuple[str], SearchType]) -> None:
    if not search_index:
        search_index={}
    if not search_source:
        search_source=[]
    if not search_info_key:
        search_info_key=tuple(" ",)
        if presenter:
            presenter.search_info.setdefault(search_info_key, dict())
    if not presenter:
        presenter=Presenter({search_info_key: dict()}, dict(), use_gui=True)
    presenter.search_info[search_info_key].setdefault(SearchInfo.MATCHED_STRINGS, list())
    presenter.search_info[search_info_key].setdefault(SearchInfo.RESULTS, list())
    search_terms=search_info_key[0]
    if search_terms[0] != " ":
        if len(search_terms) == 1:
            results=search_single_match(search_index, search_source, search_terms[0], presenter, search_info_key)
            results=unpack_list_of_sets(results)
            presenter.search_info[search_info_key][SearchInfo.RESULTS].extend(results) 
        else:
            results=search_multiple_matches(search_index, search_source, search_terms, presenter, search_info_key)
            ranked_results=rank_results(results)
            presenter.search_info[search_info_key].setdefault(SearchInfo.RESULTS, list()).extend(ranked_results)           
    presenter.prepare_results_for_presentation(search_info_key)
        
"""
Perform a search based on Levenshtein distance of search index words and search term

Calls functions that perfomr the search and organise the results into order of relevance.
Handles the presenter instance and initialises and modifies its structures in a way that
it will either hold the results, search terms and matched words or hold empty data structures
in case of errors or no results.
"""       

def search_all_with_levenshtein_distance(search_index: dict[str, set[str]], search_source: list[str], presenter: Presenter, search_info_key: tuple[tuple[str], SearchType]) -> None:    
    if not search_index:
        search_index={}
    if not search_source:
        search_source=[]
    if not search_info_key:
        search_info_key=tuple(" ",)
        if presenter:
            presenter.search_info.setdefault(search_info_key, dict())
    if not presenter:
        presenter=Presenter({search_info_key: dict()}, dict(), use_gui=True)
    presenter.search_info[search_info_key].setdefault(SearchInfo.MATCHED_STRINGS, list())
    presenter.search_info[search_info_key].setdefault(SearchInfo.RESULTS, list())
    results=search_by_levenshtein_distance(search_source, presenter, search_info_key)
    ordered_results=order_results(results, search_index)
    presenter.search_info[search_info_key][SearchInfo.RESULTS].extend(ordered_results)
    presenter.prepare_results_for_presentation(search_info_key)
    


##################################################################################################
#                                       YEAR AND ISBN SEARCH +                                   #
#                               PASS TO PRESENTER TO APPEAR ON SCREEN                            #
##################################################################################################

"""
Get the info of all matching books form a given year as a list of strings

Retrieve the set of isbns from the search index that matched the year. 
Use the set of ISBNs to create a list of strings that contain the book info
for those ISBN numbers.
"""

def year_search(year_index: dict[str, str], presenter: Presenter, search_info_key=tuple[tuple[str], SearchType]) -> None:
    if not search_info_key:
        search_info_key=tuple(" ",)
        if presenter:
            presenter.search_info.setdefault(search_info_key, dict())
    if not presenter:
        presenter=Presenter({search_info_key: dict()}, dict(), use_gui=True)
    presenter.search_info[search_info_key].setdefault(SearchInfo.MATCHED_STRINGS, list())
    presenter.search_info[search_info_key].setdefault(SearchInfo.RESULTS, list())
    if year_index and search_info_key[0][0] != " ":
        year=search_info_key[0][0]    
        isbns=year_index.get(year, []) # get the set of ISBNs corresponding to that year or an empty list if the yeare is not present in the search index
        if isbns:
            presenter.search_info[search_info_key][SearchInfo.RESULTS].extend(isbns)
            presenter.search_info[search_info_key][SearchInfo.MATCHED_STRINGS].append(year)
    presenter.prepare_results_for_presentation(search_info_key)
        
        

"""
Get the info of all matching books with a given (partial) ISBN as a list of strings

Extract and sort list of strings from book dictionary in presenter. If ISBN is between 4 and 8 
characters long, perform partial match. If ISBN is 9 or more characters (although most ISBN numbers would be 10 or 13 characters,
there are a lot of ISBNS with 9 characters in the datasets), perform
exact matching with binary search. If there is a match (or multiple matches in case
of partial match, but it is unlikely), use the ISBN(s) to create a list of strings that contain the book
info for the ISBN number(s).
"""
def isbn_search(presenter: Presenter, search_info_key: tuple[tuple[str],SearchType]) -> None:
    if not search_info_key:
        search_info_key=tuple(" ",)
        if presenter:
            presenter.search_info.setdefault(search_info_key, dict())
    if not presenter:
        presenter=Presenter({search_info_key: dict()}, dict(), use_gui=True)
    isbns=list(presenter.books.keys())
    isbns.sort()
    isbn=search_info_key[0][0]
    presenter.search_info[search_info_key].setdefault(SearchInfo.MATCHED_STRINGS, list())
    presenter.search_info[search_info_key].setdefault(SearchInfo.RESULTS, list())
    if len(isbn) >= 4 and len(isbn) < 9:
        isbns=[x for x in isbns if isbn in x] 
        presenter.search_info[search_info_key][SearchInfo.RESULTS].extend(isbns)
        presenter.search_info[search_info_key][SearchInfo.MATCHED_STRINGS].extend(isbns)       
    elif len(isbn) >=9:
    #   if books.get(isbn) is not None:
        if binary_search.binary_search(isbns, isbn)==Result.MATCH_FOUND:
            presenter.search_info[search_info_key][SearchInfo.RESULTS].append(isbn)
            presenter.search_info[search_info_key][SearchInfo.MATCHED_STRINGS].append(isbn)         
    presenter.prepare_results_for_presentation(search_info_key)
    


##################################################################################################
#                                      DETERMINE SEARCH                                          #
#                                  TYPE BASED ON SEARCH TERM                                     #
##################################################################################################
"""
Determine which search type to assign to a search term

Examines the prepared search term (list of strings) and decides
which search type is most suitable to perform. One or more strings
that do not consist of digits are assigned to word search, the 
subtype of which comes from user choice via the GUI. Strings
shorter than 4 characters are not accepted. Strings that are
exactly 4 characters long and consist of digits are assigned
year search. Strings longer between 5 and 13 characters long
that either consist of digits or match an ISBN regex pattern
are assigned ISBN search. Other edge cases are either assinged
SearchType.UNDETERMINED or handled by the function cleaning
and preparing the search term strings.
The function is used by the caller to determine which search
functions to use to perform the search or to trigger an error 
message aimed at the user in case of undetermined search type.
"""
def select_search_type(search_terms: list[str])-> SearchType:

    if not search_terms:
      return SearchType.UNDETERMINED
    
    if len(search_terms) == 1: 
        term=search_terms[0]
     
        if len(term) < 4:
            return SearchType.UNDETERMINED
        elif len(term) == 4:
            if term.isdigit():
                return SearchType.YEAR
            else:
                return SearchType.WORD
        elif len(term) > 4 and len(term) <= 13:
            if term.isdigit() or isbn_pattern.match(term) is not None:
                return SearchType.ISBN
            else:
                return SearchType.WORD
        else:
            if term.isdigit():
                return SearchType.UNDETERMINED
            else:    
                return SearchType.WORD
                     
    else:
        return SearchType.WORD 
    
