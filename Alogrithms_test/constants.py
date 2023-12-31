from enum import Enum

class BookData:
    HUNDRED_K="100kbooks.csv"
    TEN_K="10kbooks.csv"
    THOUSAND="1000books.csv"
    HUNDRED="100books.csv"
    TEN="10books.csv"

class Result:
    NOT_FOUND=-1
    MATCH_FOUND=1
    NO_BOOK="The search with the provided term(s) did not produce results"

class Search:
    LEVENSHTEIN_MAX_DISTANCE=2
    MAX_WORD_LENGTH=20
    MAX_RESULT_COUNT=100

class SearchType:
    ISBN="isbn"
    YEAR="year"
    WORD="word"
    IN="in"
    LEVENSHTEIN="levenshtein"
    UNDETERMINED="undetermined"

class SearchInfo:
    RESULTS="results"
    MATCHED_STRINGS="matched_strings"
    MATCHED_BOOK_INFO="matched_book_info"

class GraphPhotoPath(Enum):
    GRAPH_SIMPLE="graph_simple.png"
    GRAPH_MEDIUM="graph_medium.png"
    GRAPH_TREE="graph_tree.png"

    def __str__(self):
        return self.name.lower()

class GraphList(Enum):
    GRAPH_SIMPLE="graph_simple: {\n\
                                    'A': ['B', 'C'],\n\
                                    'B': ['A', 'D'],\n\
                                    'C': ['A'],\n\
                                    'D': ['B']\n\
                                }"
    GRAPH_MEDIUM="graph_medium : {\n\
                                    'A': ['B', 'C'],\n\
                                    'B': ['A', 'D', 'E'],\n\
                                    'C': ['A', 'F', 'G'],\n\
                                    'D': ['B', 'H', 'I'],\n\
                                    'E': ['B', 'J', 'K'],\n\
                                    'F': ['C', 'L', 'M'],\n\
                                    'G': ['C', 'N', 'O'],\n\
                                    'H': ['D'],\n\
                                    'I': ['D'],\n\
                                    'J': ['E'],\n\
                                    'K': ['E'],\n\
                                    'L': ['F'],\n\
                                    'M': ['F'],\n\
                                    'N': ['G'],\n\
                                    'O': ['G']\n\
                                 }"
    GRAPH_TREE="graph_tree : {\n\
                                'A': ['B', 'C'],\n\
                                'B': ['D', 'E'],\n\
                                'C': ['F', 'G'],\n\
                                'D': ['H'],\n\
                                'E': [],\n\
                                'F': [],\n\
                                'G': [],\n\
                                'H': []\n\
                             }"  

class SortingAlgorithm(Enum):
    BUBBLE="bubble_sort"
    MERGE="merge_sort"

