import unittest
from graph_matrix import init_matrix, populate_matrix
from book_data import get_book_titles_from_csv, create_books_from_csv
from new_search_util import *
from binary_search import *
from levenshtein_distance import levenshtein_distance
from presenter import *


class TestGraphMatrix(unittest.TestCase):
    def test_init_matrix(self):
        test_dict = {"A": 1, "B": 2, "C": 3, "D": 4}
        expected_matrix = [
            ["", "A", "B", "C", "D"],
            ["A", "", "", "", ""],
            ["B", "", "", "", ""],
            ["C", "", "", "", ""],
            ["D", "", "", "", ""]
        ]
        result_matrix = init_matrix(test_dict)
        self.assertEqual(result_matrix, expected_matrix)
    
    def test_populate_matrix(self):
        test_graph = {
                        "A": ["B", "C"],
                        "B": ["A", "D"],
                        "C": ["A"],
                        "D": ["B"]
                     }
        initial_matrix = [
            ["", "A", "B", "C", "D"],
            ["A", "", "", "", ""],
            ["B", "", "", "", ""],
            ["C", "", "", "", ""],
            ["D", "", "", "", ""]
        ]
        expected_matrix = [
            ["", "A", "B", "C", "D"],
            ["A", 0, 1, 1, 0],
            ["B", 1, 0, 0, 1],
            ["C", 1, 0, 0, 0],
            ["D", 0, 1, 0, 0]
        ]

        populate_matrix(initial_matrix, test_graph)
        self.assertEqual(initial_matrix, expected_matrix)

class TestSortTest(unittest.TestCase):
    def test_get_book_titles_from_csv(self):
        test_path = "10books.csv"
        expected_list = [
                            "Classical Mythology",
                            "Clara Callan",
                            "Decision in Normandy",
                            "Flu: The Story of the Great Influenza Pandemic of 1918 and the Search for the Virus That Caused It",
                            "The Mummies of Urumchi",
                            "The Kitchen God's Wife",
                            "What If?: The World's Foremost Military Historians Imagine What Might Have Been",
                            "PLEADING GUILTY",
                            "Under the Black Flag: The Romance and the Reality of Life Among the Pirates",
                            "Where You'll Find Me: And Other Stories"
                        ]
        result_list = get_book_titles_from_csv(test_path)
        self.assertEqual(result_list, expected_list)

class TestBookData(unittest.TestCase):
    unittest.TestCase.maxDiff = None
    def test_create_books_from_csv(self):
        test_path="10books.csv"
        expected_books={"195153448": {"Title": "Classical Mythology", "Author": "Mark P. O. Morford", "Publisher": "Oxford University Press", "Year": "2002"},
                        "2005018": {"Title": "Clara Callan", "Author": "Richard Bruce Wright", "Publisher": "HarperFlamingo Canada", "Year": "2001"},
                        "60973129": {"Title": "Decision in Normandy", "Author": "Carlo D'Este", "Publisher": "HarperPerennial", "Year": "1991"},
                        "374157065": {"Title": "Flu: The Story of the Great Influenza Pandemic of 1918 and the Search for the Virus That Caused It", "Author": "Gina Bari Kolata", "Publisher": "Farrar Straus Giroux", "Year": "1999"},
                        "393045218": {"Title": "The Mummies of Urumchi", "Author": "E. J. W. Barber", "Publisher": "W. W. Norton &amp; Company", "Year": "1999"},
                        "399135782": {"Title": "The Kitchen God's Wife", "Author": "Amy Tan", "Publisher": "Putnam Pub Group", "Year": "1991"},
                        "425176428": {"Title": "What If?: The World's Foremost Military Historians Imagine What Might Have Been", "Author": "Robert Cowley", "Publisher": "Berkley Publishing Group", "Year": "2000"},
                        "671870432": {"Title": "PLEADING GUILTY", "Author": "Scott Turow", "Publisher": "Audioworks", "Year": "1993"},
                        "679425608": {"Title": "Under the Black Flag: The Romance and the Reality of Life Among the Pirates", "Author": "David Cordingly", "Publisher": "Random House", "Year": "1996"},
                        "074322678X": {"Title": "Where You'll Find Me: And Other Stories", "Author": "Ann Beattie", "Publisher": "Scribner", "Year": "2002"}}
        result_books=create_books_from_csv(test_path)    
        self.assertEqual(result_books, expected_books  )

class TestBinarySearch(unittest.TestCase):
    def test_binary_search(self):
        test_words=["apple", "banana", "cherry", "kiwi", "lime"]
        test_ints=[1,2,3,4,5,6,7,8,9]
        test_mixed=["apple", 1]
        test_string_year=["2001", "2005", "2011", "2015", "2021", "2023"]
        self.assertEqual(binary_search(test_words, "pineapple"), Result.NOT_FOUND)
        self.assertEqual(binary_search(test_ints, 3), Result.MATCH_FOUND)
        self.assertEqual(binary_search(test_ints, 111), Result.NOT_FOUND)
        self.assertEqual(binary_search(test_words, "kiwi"), Result.MATCH_FOUND)
        self.assertEqual(binary_search(test_mixed, 1), Result.NOT_FOUND)
        self.assertEqual(binary_search([], 1), Result.NOT_FOUND)
        self.assertEqual(binary_search(test_string_year, "2015"), Result.MATCH_FOUND)

class TestBinarySearchByStringLength(unittest.TestCase):
    def test_binary_search_by_string_length(self):
        test_words=["kiwi", "kiwi", "kiwi", "apple", "apple", "apple", "banana", "banana", "banana"]
        test_words.sort(key=len)
        self.assertEqual(binary_search_by_string_length(test_words, 4), 0)
        self.assertEqual(binary_search_by_string_length(test_words, 5), 3) 
        self.assertEqual(binary_search_by_string_length(test_words, 6), 6) 
        self.assertEqual(binary_search_by_string_length(test_words, 50), -1) 
        self.assertEqual(binary_search_by_string_length(test_words, 3.55), -1) 
        self.assertEqual(binary_search_by_string_length(test_words, "something"), -1) 

class TestLevenshteinDistance(unittest.TestCase):
    def test_levenshtein_distance(self):
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
        self.assertEqual(levenshtein_distance("author", "author"), 0)
        self.assertEqual(levenshtein_distance("",""), 0)
        self.assertEqual(levenshtein_distance("author", "5"), 6)
        self.assertEqual(levenshtein_distance("author", 5), -1)
        self.assertEqual(levenshtein_distance("author", 5), Result.NOT_FOUND)
        
class TestRemoveSpecialCharacters(unittest.TestCase):
    def test_remove_special_characters(self):
        self.assertEqual(remove_special_characters("@He_llo# world!"), "Hello world")
        self.assertEqual(remove_special_characters("Nothing to remove"), "Nothing to remove")
        self.assertEqual(remove_special_characters(""), "")
        self.assertEqual(remove_special_characters("_-=+|/.@;:, "), " ")

class TestPrepareString(unittest.TestCase):
    def test_prepare_string(self):
        self.assertEqual(prepare_string("  The q@uick brown! FOX jumps _over the lazy dog  "), ["quick", "brown", "fox", "jumps", "lazy", "dog"])
        self.assertEqual(prepare_string("  *&%$ and or it the "), [])
        self.assertEqual(prepare_string("2015-2017"), ["20152017"])

class TestSearchSingleMatch(unittest.TestCase):
    def test_search_single_match(self):
        test_search_index={"classical": {"195153448"}, "mythology": {"195153448"}, "mark": {"195153448"}, 
                          "morford": {"195153448"}, "oxford": {"195153448"}, "university": {"195153448"}, 
                          "press": {"195153448"}, "clara": {"2005018"}, "callan": {"2005018"}, 
                          "richard": {"2005018"}, "bruce": {"2005018"}, "wright": {"2005018"}, 
                          "harperflamingo": {"2005018"}, "canada": {"2005018"}, "decision": {"60973129"}, 
                          "normandy": {"60973129"}, "carlo": {"60973129"}, "deste": {"60973129"}, 
                          "harperperennial": {"60973129"}, "flu": {"374157065"}, "story": {"374157065"}, 
                          "great": {"374157065"}, "influenza": {"374157065"}, "pandemic": {"374157065"}, 
                          "1918": {"374157065"}, "search": {"374157065"}, "virus": {"374157065"}, 
                          "caused": {"374157065"}, "gina": {"374157065"}, "bari": {"374157065"}, 
                          "kolata": {"374157065"}, "farrar": {"374157065"}, "straus": {"374157065"}, 
                          "giroux": {"374157065"}, "mummies": {"393045218"}, "urumchi": {"393045218"}, 
                          "barber": {"393045218"}, "norton": {"393045218"}, "amp": {"393045218"}, 
                          "company": {"393045218"}, "kitchen": {"399135782"}, "gods": {"399135782"}, 
                          "wife": {"399135782"}, "amy": {"399135782"}, "tan": {"399135782"}, 
                          "putnam": {"399135782"}, "pub": {"399135782"}, "group": {"425176428", "399135782"}, 
                          "worlds": {"425176428"}, "foremost": {"425176428"}, "military": {"425176428"}, 
                          "historians": {"425176428"}, "imagine": {"425176428"}, "might": {"425176428"}, 
                          "robert": {"425176428"}, "cowley": {"425176428"}, "berkley": {"425176428"}, 
                          "publishing": {"425176428"}, "pleading": {"671870432"}, "guilty": {"671870432"}, 
                          "scott": {"671870432"}, "turow": {"671870432"}, "audioworks": {"671870432"}, 
                          "black": {"679425608"}, "flag": {"679425608"}, "romance": {"679425608"}, 
                          "reality": {"679425608"}, "life": {"679425608"}, "among": {"679425608"}, 
                          "pirates": {"679425608"}, "david": {"679425608"}, "cordingly": {"679425608"}, 
                          "random": {"679425608"}, "house": {"679425608"}, "youll": {"074322678X"}, 
                          "find": {"074322678X"}, "stories": {"074322678X"}, "ann": {"074322678X"}, 
                          "beattie": {"074322678X"}, "scribner": {"074322678X"}}
        test_search_source=list(test_search_index.keys())
        test_search_source.sort(key=len)
        search_info_key=(("group"), SearchType.IN)
        presenter=Presenter({search_info_key: dict()}, dict(), use_gui=False)  
        self.assertEqual(search_single_match(test_search_index, test_search_source, "group", presenter, search_info_key), [{"399135782", "425176428"}])
        search_info_key=((""), SearchType.IN)
        presenter.search_info.setdefault(search_info_key, dict())
        self.assertEqual(search_single_match(test_search_index, test_search_source, "", presenter, search_info_key), [])
        search_info_key=(("lar"), SearchType.IN)
        presenter.search_info.setdefault(search_info_key, dict())
        self.assertEqual(search_single_match(test_search_index, test_search_source, "lar", presenter, search_info_key), [{"2005018"}])
        search_info_key=((""), SearchType.IN)
        presenter.search_info.setdefault(search_info_key, dict())
        self.assertEqual(search_single_match(test_search_index, test_search_source, 5, presenter, search_info_key), [])
        search_info_key=(("life"), SearchType.IN)
        presenter.search_info.setdefault(search_info_key, dict())
        self.assertEqual(search_single_match({}, test_search_source, "life", presenter, search_info_key), [])

class TestUnpackListOfSets(unittest.TestCase):
    def test_unpack_list_of_sets(self):
        self.assertCountEqual(unpack_list_of_sets([{123456, 34567}, {998866}, {1}]), [34567, 123456, 998866, 1])
        self.assertCountEqual(unpack_list_of_sets([{1, 2}, {}, {3}]), [1, 2, 3])
        self.assertCountEqual(unpack_list_of_sets([{"1", "2"}, {}, {"3"}]), ["1", "2", "3"])
        self.assertEqual(unpack_list_of_sets([]), [])

class TestSearchMultipleMatches(unittest.TestCase):
    def test_search_multiple_matches(self):
        test_search_index={"classical": {"195153448"}, "mythology": {"195153448"}, "mark": {"195153448"}, 
                          "morford": {"195153448"}, "oxford": {"195153448"}, "university": {"195153448"}, 
                          "press": {"195153448"}, "clara": {"2005018"}, "callan": {"2005018"}, 
                          "richard": {"2005018"}, "bruce": {"2005018"}, "wright": {"2005018"}, 
                          "harperflamingo": {"2005018"}, "canada": {"2005018"}, "decision": {"60973129"}, 
                          "normandy": {"60973129"}, "carlo": {"60973129"}, "deste": {"60973129"}, 
                          "harperperennial": {"60973129"}, "flu": {"374157065"}, "story": {"374157065"}, 
                          "great": {"374157065"}, "influenza": {"374157065"}, "pandemic": {"374157065"}, 
                          "1918": {"374157065"}, "search": {"374157065"}, "virus": {"374157065"}, 
                          "caused": {"374157065"}, "gina": {"374157065"}, "bari": {"374157065"}, 
                          "kolata": {"374157065"}, "farrar": {"374157065"}, "straus": {"374157065"}, 
                          "giroux": {"374157065"}, "mummies": {"393045218"}, "urumchi": {"393045218"}, 
                          "barber": {"393045218"}, "norton": {"393045218"}, "amp": {"393045218"}, 
                          "company": {"393045218"}, "kitchen": {"399135782"}, "gods": {"399135782"}, 
                          "wife": {"399135782"}, "amy": {"399135782"}, "tan": {"399135782"}, 
                          "putnam": {"399135782"}, "pub": {"399135782"}, "group": {"425176428", "399135782"}, 
                          "worlds": {"425176428"}, "foremost": {"425176428"}, "military": {"425176428"}, 
                          "historians": {"425176428"}, "imagine": {"425176428"}, "might": {"425176428"}, 
                          "robert": {"425176428"}, "cowley": {"425176428"}, "berkley": {"425176428"}, 
                          "publishing": {"425176428"}, "pleading": {"671870432"}, "guilty": {"671870432"}, 
                          "scott": {"671870432"}, "turow": {"671870432"}, "audioworks": {"671870432"}, 
                          "black": {"679425608"}, "flag": {"679425608"}, "romance": {"679425608"}, 
                          "reality": {"679425608"}, "life": {"679425608"}, "among": {"679425608"}, 
                          "pirates": {"679425608"}, "david": {"679425608"}, "cordingly": {"679425608"}, 
                          "random": {"679425608"}, "house": {"679425608"}, "youll": {"074322678X"}, 
                          "find": {"074322678X"}, "stories": {"074322678X"}, "ann": {"074322678X"}, 
                          "beattie": {"074322678X"}, "scribner": {"074322678X"}}
        test_search_source=list(test_search_index.keys())
        test_search_source.sort(key=len)
        search_info_key=(("mummies", "kitchen"), SearchType.IN)
        presenter=Presenter({search_info_key: dict()}, dict(), use_gui=False)
        self.assertEqual(search_multiple_matches(test_search_index, test_search_source, ["mummies", "kitchen"], presenter, search_info_key), [{"393045218"}, {"399135782"}])
        self.assertEqual(search_multiple_matches({}, test_search_source, ["mummies", "kitchen"], presenter, search_info_key), [])
        self.assertEqual(search_multiple_matches(test_search_index, [], ["mummies", "kitchen"], presenter, search_info_key), [])
        search_info_key=((), "")
        presenter.search_info.setdefault(search_info_key, dict())
        self.assertEqual(search_multiple_matches(test_search_index, test_search_source, [], presenter, search_info_key ), [])
        search_info_key=(("noisy", "historians"), SearchType.IN)
        presenter.search_info.setdefault(search_info_key, dict())
        self.assertEqual(search_multiple_matches(test_search_index, test_search_source, ["noisy", "historians"], presenter, search_info_key), [{"425176428"}])

class TestElementsInIntersections(unittest.TestCase):
    def test_elements_in_intersections(self):
        test_sets=[{1,2,7,8,11,12}, {3,4,7,8,9,10,11,12}, {5,6,9,10,11,12}]
        test_disjoint_sets=[{1,2,3}, {4,5,6}, {7,8,9}]
        self.assertEqual(elements_in_intersections(test_sets, 2, {11, 12}), [{7,8},{9,10}])
        self.assertEqual(elements_in_intersections(test_disjoint_sets, 2, set()), [])
        self.assertEqual(elements_in_intersections([], 2, set()), [])
        self.assertEqual(elements_in_intersections(test_sets, -1, {11,12}), [])

class TestFindAllElementsInIntersections(unittest.TestCase):
    def test_find_all_elements_in_intersections(self):
        test_sets=[{1,2,7,8,11,12}, {3,4,7,8,9,10,11,12}, {5,6,9,10,11,12}]
        test_disjoint_sets=[{1,2,3}, {4,5,6}, {7,8,9}]
        test_string_sets=[{"apple", "banana"}, {"apple", "kiwi", "cherry"}, {"apple"}, {"apple", "cherry"} ]
        self.assertEqual(find_all_elements_in_intersections(test_sets),[{11,12}, {7,8}, {9,10}])
        self.assertEqual(find_all_elements_in_intersections(test_string_sets), [{"apple"}, {"cherry"}])
        self.assertEqual(find_all_elements_in_intersections(test_disjoint_sets), [])
        self.assertEqual(find_all_elements_in_intersections([]), [])

class TestFindAllSetDifferences(unittest.TestCase):
    def test_find_all_set_differences(self):
        test_sets=[{1,2,7,8,11,12}, {3,4,7,8,9,10,11,12}, {5,6,9,10,11,12}]
        test_disjoint_sets=[{1,2,3}, {4,5,6}, {7,8,9}]
        test_string_sets=[{"apple", "banana"}, {"apple", "kiwi"}, {"apple"}, {"apple", "cherry"} ]
        self.assertCountEqual(find_all_set_differences(test_sets, [11,12,10,9,8,7]), [1,2,3,4,5,6])
        self.assertCountEqual(find_all_set_differences(test_disjoint_sets, []), [1,2,3,4,5,6,7,8,9])
        self.assertCountEqual(find_all_set_differences(test_string_sets, ["apple"]), ["banana", "cherry", "kiwi"])
        self.assertEqual(find_all_set_differences([], [1,2,3]), [])

class TestRankResults(unittest.TestCase):
    def test_rank_results(self):
        test_results=[{"1","2","7","8","11","12"}, {"3","4","7","8","9","10","11","12"}, {"5","6","9","10","11","12"}]
        test_results_disjoint=[{"123", "234"}, {"567", "345"}, {"133"}]
        self.assertCountEqual(rank_results(test_results), ["11", "12", "7", "8", "10", "9", "1", "2", "3", "4", "5", "6" ])
        self.assertCountEqual(rank_results(test_results_disjoint), ["123", "133", "234", "345", "567"])
        self.assertEqual(rank_results([]), [])

class TestSliceListForLevenshteinSearch(unittest.TestCase):
    def test_slice_list_for_levenshtein_search(self):
        test_words=["flu", "amp", "amy", "tan", "pub", "ann", "mark", "1918", "gina", "bari", "gods", "wife", 
                   "flag", "life", "find", "press", "clara", "bruce", "carlo", "deste", "story", "great", 
                   "virus", "group", "might", "scott", "turow", "black", "among", "david", "house", "youll", 
                   "oxford", "callan", "wright", "canada", "search", "caused", "kolata", "farrar", "straus", 
                   "giroux", "barber", "norton", "putnam", "worlds", "robert", "cowley", "guilty", "random", 
                   "morford", "richard", "mummies", "urumchi", "company", "kitchen", "imagine", "berkley", 
                   "romance", "reality", "pirates", "stories", "beattie", "decision", "normandy", "pandemic", 
                   "foremost", "military", "pleading", "scribner", "classical", "mythology", "influenza", 
                   "cordingly", "university", "historians", "publishing", "audioworks", "harperflamingo", 
                   "harperperennial"]
        self.assertEqual(slice_list_for_levenshtein_search(test_words, 3), ["flu", "amp", "amy", "tan", "pub", "ann", 
                                                                            "mark", "1918", "gina", "bari", "gods", "wife", 
                                                                            "flag", "life", "find", "press", "clara", "bruce", 
                                                                            "carlo", "deste", "story", "great", "virus", "group", 
                                                                            "might", "scott", "turow", "black", "among", "david", 
                                                                            "house", "youll"])
        self.assertEqual(slice_list_for_levenshtein_search(test_words, -1), test_words)
        self.assertEqual(slice_list_for_levenshtein_search(test_words, 1000), test_words)
        self.assertEqual(slice_list_for_levenshtein_search([], 4), [])
        self.assertEqual(slice_list_for_levenshtein_search(test_words, "hello"), test_words)

class TestSearchByLevenshteinDistance(unittest.TestCase):
    def test_search_by_levenshtein_distance(self):
         test_search_index={"classical": {"195153448"}, "mythology": {"195153448"}, "mark": {"195153448"}, 
                            "morford": {"195153448"}, "oxford": {"195153448"}, "university": {"195153448"}, 
                            "press": {"195153448"}, "clara": {"2005018"}, "callan": {"2005018"}, 
                            "richard": {"2005018"}, "bruce": {"2005018"}, "wright": {"2005018"}, 
                            "harperflamingo": {"2005018"}, "canada": {"2005018"}, "decision": {"60973129"}, 
                            "normandy": {"60973129"}, "carlo": {"60973129"}, "deste": {"60973129"}, 
                            "harperperennial": {"60973129"}, "flu": {"374157065"}, "story": {"374157065"}, 
                            "great": {"374157065"}, "influenza": {"374157065"}, "pandemic": {"374157065"}, 
                            "1918": {"374157065"}, "search": {"374157065"}, "virus": {"374157065"}, 
                            "caused": {"374157065"}, "gina": {"374157065"}, "bari": {"374157065"}, 
                            "kolata": {"374157065"}, "farrar": {"374157065"}, "straus": {"374157065"}, 
                            "giroux": {"374157065"}, "mummies": {"393045218"}, "urumchi": {"393045218"}, 
                            "barber": {"393045218"}, "norton": {"393045218"}, "amp": {"393045218"}, 
                            "company": {"393045218"}, "kitchen": {"399135782"}, "gods": {"399135782"}, 
                            "wife": {"399135782"}, "amy": {"399135782"}, "tan": {"399135782"}, 
                            "putnam": {"399135782"}, "pub": {"399135782"}, "group": {"425176428", "399135782"}, 
                            "worlds": {"425176428"}, "foremost": {"425176428"}, "military": {"425176428"}, 
                            "historians": {"425176428"}, "imagine": {"425176428"}, "might": {"425176428"}, 
                            "robert": {"425176428"}, "cowley": {"425176428"}, "berkley": {"425176428"}, 
                            "publishing": {"425176428"}, "pleading": {"671870432"}, "guilty": {"671870432"}, 
                            "scott": {"671870432"}, "turow": {"671870432"}, "audioworks": {"671870432"}, 
                            "black": {"679425608"}, "flag": {"679425608"}, "romance": {"679425608"}, 
                            "reality": {"679425608"}, "life": {"679425608"}, "among": {"679425608"}, 
                            "pirates": {"679425608"}, "david": {"679425608"}, "cordingly": {"679425608"}, 
                            "random": {"679425608"}, "house": {"679425608"}, "youll": {"074322678X"}, 
                            "find": {"074322678X"}, "stories": {"074322678X"}, "ann": {"074322678X"}, 
                            "beattie": {"074322678X"}, "scribner": {"074322678X"}}
         test_words_to_search=list(test_search_index.keys())
         search_info_key=(("reality", "militry", "accordingly"), SearchType.LEVENSHTEIN)
         presenter=Presenter({search_info_key: dict()}, dict(), use_gui=False)
         expected_results_1={0: ["reality"], 1:["military"], 2:["cordingly"]}
         search_info_key_2=(("realit", "militry", "crdingly"), SearchType.LEVENSHTEIN)
         presenter_2=Presenter({search_info_key_2: dict()}, dict(), use_gui=False)
         expected_results_2={1: ["reality", "military", "cordingly"]}
         self.assertEqual(search_by_levenshtein_distance(test_words_to_search, presenter, search_info_key), expected_results_1)
         self.assertEqual(search_by_levenshtein_distance(test_words_to_search, presenter_2, search_info_key_2), expected_results_2)
         self.assertEqual(search_by_levenshtein_distance([], presenter, search_info_key), {})
         self.assertEqual(search_by_levenshtein_distance(test_words_to_search, None, search_info_key), {})
         self.assertEqual(search_by_levenshtein_distance(test_words_to_search, presenter, tuple()), {})

class TestOrderResults(unittest.TestCase):
    def test_order_results(self):
        test_search_index={"classical": {"195153448"}, "mythology": {"195153448"}, "mark": {"195153448"}, 
                          "morford": {"195153448"}, "oxford": {"195153448"}, "university": {"195153448"}, 
                          "press": {"195153448"}, "clara": {"2005018"}, "callan": {"2005018"}, 
                          "richard": {"2005018"}, "bruce": {"2005018"}, "wright": {"2005018"}, 
                          "harperflamingo": {"2005018"}, "canada": {"2005018"}, "decision": {"60973129"}, 
                          "normandy": {"60973129"}, "carlo": {"60973129"}, "deste": {"60973129"}, 
                          "harperperennial": {"60973129"}, "flu": {"374157065"}, "story": {"374157065"}, 
                          "great": {"374157065"}, "influenza": {"374157065"}, "pandemic": {"374157065"}, 
                          "1918": {"374157065"}, "search": {"374157065"}, "virus": {"374157065"}, 
                          "caused": {"374157065"}, "gina": {"374157065"}, "bari": {"374157065"}, 
                          "kolata": {"374157065"}, "farrar": {"374157065"}, "straus": {"374157065"}, 
                          "giroux": {"374157065"}, "mummies": {"393045218"}, "urumchi": {"393045218"}, 
                          "barber": {"393045218"}, "norton": {"393045218"}, "amp": {"393045218"}, 
                          "company": {"393045218"}, "kitchen": {"399135782"}, "gods": {"399135782"}, 
                          "wife": {"399135782"}, "amy": {"399135782"}, "tan": {"399135782"}, 
                          "putnam": {"399135782"}, "pub": {"399135782"}, "group": {"425176428", "399135782"}, 
                          "worlds": {"425176428"}, "foremost": {"425176428"}, "military": {"425176428"}, 
                          "historians": {"425176428"}, "imagine": {"425176428"}, "might": {"425176428"}, 
                          "robert": {"425176428"}, "cowley": {"425176428"}, "berkley": {"425176428"}, 
                          "publishing": {"425176428"}, "pleading": {"671870432"}, "guilty": {"671870432"}, 
                          "scott": {"671870432"}, "turow": {"671870432"}, "audioworks": {"671870432"}, 
                          "black": {"679425608"}, "flag": {"679425608"}, "romance": {"679425608"}, 
                          "reality": {"679425608"}, "life": {"679425608"}, "among": {"679425608"}, 
                          "pirates": {"679425608"}, "david": {"679425608"}, "cordingly": {"679425608"}, 
                          "random": {"679425608"}, "house": {"679425608"}, "youll": {"074322678X"}, 
                          "find": {"074322678X"}, "stories": {"074322678X"}, "ann": {"074322678X"}, 
                          "beattie": {"074322678X"}, "scribner": {"074322678X"}}
        test_search_results={0: ["reality", "wife"], 1:["military", "romance"], 2:["cordingly", "guilty"]}
        expected_output=["399135782", "679425608", "425176428", "679425608", "671870432", "679425608"]
        self.assertCountEqual(order_results(test_search_results, test_search_index), expected_output)
        self.assertEqual(order_results({}, test_search_index), [])
        self.assertEqual(order_results(test_search_results, {}), [])

class TestYearSearch(unittest.TestCase):
    def test_year_search(self):
        test_year_index={
                         "2002": {"074322678X", "195153448"}, 
                         "2001": {"2005018"}, 
                         "1991": {"60973129", "399135782"}, 
                         "1999": {"374157065", "393045218"}, 
                         "2000": {"425176428"}, 
                         "1993": {"671870432"}, 
                         "1996": {"679425608"}
                         }
        test_books={
                    "195153448": {"Title": "Classical Mythology", "Author": "Mark P. O. Morford", "Publisher": "Oxford University Press", "Year": "2002"},
                    "2005018": {"Title": "Clara Callan", "Author": "Richard Bruce Wright", "Publisher": "HarperFlamingo Canada", "Year": "2001"},
                    "60973129": {"Title": "Decision in Normandy", "Author": "Carlo D'Este", "Publisher": "HarperPerennial", "Year": "1991"},
                    "374157065": {"Title": "Flu: The Story of the Great Influenza Pandemic of 1918 and the Search for the Virus That Caused It", "Author": "Gina Bari Kolata", "Publisher": "Farrar Straus Giroux", "Year": "1999"},
                    "393045218": {"Title": "The Mummies of Urumchi", "Author": "E. J. W. Barber", "Publisher": "W. W. Norton &amp; Company", "Year": "1999"},
                    "399135782": {"Title": "The Kitchen God's Wife", "Author": "Amy Tan", "Publisher": "Putnam Pub Group", "Year": "1991"},
                    "425176428": {"Title": "What If?: The World's Foremost Military Historians Imagine What Might Have Been", "Author": "Robert Cowley", "Publisher": "Berkley Publishing Group", "Year": "2000"},
                    "671870432": {"Title": "PLEADING GUILTY", "Author": "Scott Turow", "Publisher": "Audioworks", "Year": "1993"},
                    "679425608": {"Title": "Under the Black Flag: The Romance and the Reality of Life Among the Pirates", "Author": "David Cordingly", "Publisher": "Random House", "Year": "1996"},
                    "074322678X": {"Title": "Where You'll Find Me: And Other Stories", "Author": "Ann Beattie", "Publisher": "Scribner", "Year": "2002"}
                    }
        search_info_key=(("2002",), SearchType.YEAR)
        presenter=Presenter({search_info_key: dict()}, test_books, use_gui=False)
        result=year_search(test_year_index, presenter, search_info_key)
        self.assertIsNone(result)
        self.assertCountEqual(presenter.search_info[search_info_key][SearchInfo.RESULTS], ["074322678X", "195153448"])
        search_info_key=(("1985",), SearchType.YEAR)
        presenter.search_info.setdefault(search_info_key, dict())
        year_search(test_year_index, presenter, search_info_key)
        self.assertEqual(presenter.search_info[search_info_key][SearchInfo.RESULTS], [])
        search_info_key=tuple()
        presenter.search_info.setdefault(search_info_key, dict())
        year_search(test_year_index, presenter, search_info_key)
        search_info_key=tuple(" ",)
        self.assertEqual(presenter.search_info[search_info_key][SearchInfo.RESULTS], [])
        
class TestIsbnSearch(unittest.TestCase):
    def test_isbn_search(self):
        test_books={
                    "195153448": {"Title": "Classical Mythology", "Author": "Mark P. O. Morford", "Publisher": "Oxford University Press", "Year": "2002"},
                    "2005018": {"Title": "Clara Callan", "Author": "Richard Bruce Wright", "Publisher": "HarperFlamingo Canada", "Year": "2001"},
                    "60973129": {"Title": "Decision in Normandy", "Author": "Carlo D'Este", "Publisher": "HarperPerennial", "Year": "1991"},
                    "374157065": {"Title": "Flu: The Story of the Great Influenza Pandemic of 1918 and the Search for the Virus That Caused It", "Author": "Gina Bari Kolata", "Publisher": "Farrar Straus Giroux", "Year": "1999"},
                    "393045218": {"Title": "The Mummies of Urumchi", "Author": "E. J. W. Barber", "Publisher": "W. W. Norton &amp; Company", "Year": "1999"},
                    "399135782": {"Title": "The Kitchen God's Wife", "Author": "Amy Tan", "Publisher": "Putnam Pub Group", "Year": "1991"},
                    "425176428": {"Title": "What If?: The World's Foremost Military Historians Imagine What Might Have Been", "Author": "Robert Cowley", "Publisher": "Berkley Publishing Group", "Year": "2000"},
                    "671870432": {"Title": "PLEADING GUILTY", "Author": "Scott Turow", "Publisher": "Audioworks", "Year": "1993"},
                    "679425608": {"Title": "Under the Black Flag: The Romance and the Reality of Life Among the Pirates", "Author": "David Cordingly", "Publisher": "Random House", "Year": "1996"},
                    "074322678X": {"Title": "Where You'll Find Me: And Other Stories", "Author": "Ann Beattie", "Publisher": "Scribner", "Year": "2002"}
                    }
        search_info_key=(("60973129",), SearchType.ISBN)
        presenter=Presenter({search_info_key: dict()}, test_books, use_gui=False)
        result=isbn_search(presenter, search_info_key)
        self.assertIsNone(result)
        self.assertEqual(presenter.search_info[search_info_key][SearchInfo.RESULTS], ["60973129"])
        search_info_key=(("19515",), SearchType.ISBN)
        presenter.search_info.setdefault(search_info_key, dict())
        isbn_search(presenter, search_info_key)
        self.assertEqual(presenter.search_info[search_info_key][SearchInfo.RESULTS], ["195153448"])
        search_info_key=(("2678X",), SearchType.ISBN)
        presenter.search_info.setdefault(search_info_key, dict())
        isbn_search(presenter, search_info_key)
        self.assertEqual(presenter.search_info[search_info_key][SearchInfo.RESULTS], ["074322678X"])
        
class TestPrepareResultsForPresentation(unittest.TestCase):
    def test_prepare_results_for_presentation(self):
        test_isbns=["393045218", "671870432"]
        test_books={
                    "195153448": {"Title": "Classical Mythology", "Author": "Mark P. O. Morford", "Publisher": "Oxford University Press", "Year": "2002"},
                    "2005018": {"Title": "Clara Callan", "Author": "Richard Bruce Wright", "Publisher": "HarperFlamingo Canada", "Year": "2001"},
                    "60973129": {"Title": "Decision in Normandy", "Author": "Carlo D'Este", "Publisher": "HarperPerennial", "Year": "1991"},
                    "374157065": {"Title": "Flu: The Story of the Great Influenza Pandemic of 1918 and the Search for the Virus That Caused It", "Author": "Gina Bari Kolata", "Publisher": "Farrar Straus Giroux", "Year": "1999"},
                    "393045218": {"Title": "The Mummies of Urumchi", "Author": "E. J. W. Barber", "Publisher": "W. W. Norton &amp; Company", "Year": "1999"},
                    "399135782": {"Title": "The Kitchen God's Wife", "Author": "Amy Tan", "Publisher": "Putnam Pub Group", "Year": "1991"},
                    "425176428": {"Title": "What If?: The World's Foremost Military Historians Imagine What Might Have Been", "Author": "Robert Cowley", "Publisher": "Berkley Publishing Group", "Year": "2000"},
                    "671870432": {"Title": "PLEADING GUILTY", "Author": "Scott Turow", "Publisher": "Audioworks", "Year": "1993"},
                    "679425608": {"Title": "Under the Black Flag: The Romance and the Reality of Life Among the Pirates", "Author": "David Cordingly", "Publisher": "Random House", "Year": "1996"},
                    "074322678X": {"Title": "Where You'll Find Me: And Other Stories", "Author": "Ann Beattie", "Publisher": "Scribner", "Year": "2002"}
                   }
        search_info_key=(("mummies", "guilty"), SearchType.WORD)
        presenter=Presenter({search_info_key: {"results": test_isbns, "matched words": test_isbns}}, test_books, use_gui=False)
        expected_book_info=[
                            [
                            "ISBN: 393045218", 
                            "Title: The Mummies of Urumchi", 
                            "Author: E. J. W. Barber", 
                            "Publisher: W. W. Norton &amp; Company", 
                            "Year: 1999"
                            ],
                            [
                            "ISBN: 671870432",
                            "Title: PLEADING GUILTY", 
                            "Author: Scott Turow", 
                            "Publisher: Audioworks", 
                            "Year: 1993"
                            ]
                           ]
        
        result=presenter.prepare_results_for_presentation(search_info_key)
        self.assertIsNone(result)
        self.assertEqual(presenter.search_info[search_info_key][SearchInfo.MATCHED_BOOK_INFO], expected_book_info)
        search_info_key=(" ",)
        presenter.search_info.setdefault(search_info_key, dict()).setdefault(SearchInfo.RESULTS, list())
        presenter.prepare_results_for_presentation(search_info_key)
        self.assertEqual(presenter.search_info[search_info_key][SearchInfo.MATCHED_BOOK_INFO], [])     

class TestSelectSearchType(unittest.TestCase):
    def test_select_search_type(self):
        self.assertEqual(select_search_type(["1991"]), SearchType.YEAR)
        self.assertEqual(select_search_type(["1"]), SearchType.UNDETERMINED)
        self.assertEqual(select_search_type(["10945"]), SearchType.ISBN)
        self.assertEqual(select_search_type(["1094511584789"]), SearchType.ISBN)
        self.assertEqual(select_search_type(["109451158478999  k,"]), SearchType.WORD)
        self.assertEqual(select_search_type(["urumchi"]), SearchType.WORD)
        self.assertEqual(select_search_type(["mummies", "urumchi"]), SearchType.WORD)
        self.assertEqual(select_search_type([]), SearchType.UNDETERMINED)
                
"""
def run_tests():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestGraphMatrix("test_init_matrix"))
    runner = unittest.TextTestRunner()
    runner.run(test_suite)

run_tests()

"""

if __name__=="__main__":
    unittest.main(verbosity=2)