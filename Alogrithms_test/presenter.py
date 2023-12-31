from tkinter import *
from tkinter.font import Font
from constants import *

"""
A class to hold search info and results and format results
to present on the screen
"""
class Presenter():
    """
    The main component of a Presenter object is the search_info, which is 
    a nested dictionary that holds all the search info that is needed to
    identify a search with its results and to identify which words need to
    be highlighted within search results when presented on the screen.

    The search_info: contain a tuple:dictionary pairs, of which the tuple
    is referred to as "search_info_key" throughout the program. The
    search_info_key contains two elements: an inner tuple that contains
    the relevant words of the search term, and the SearchType constant. These
    combined sufficiently identify a search. The dictionary identified by 
    the search_info_key holds the matched words, results (ISBNs of matched
    books) and matched book info related to the search. A simple example of
    a search_info dictionary after a word search: 
    {
        (("mummies",), SearchType.LEVENSHTEIN): ---> this is the search_info_key
            {
             SearchInfo.MATCHED_WORDS:["mummies"],
             SearchInfo.RESULTS:["393045218"], 
             SearchInfo.MATCHED_BOOK_INFO:[
                                  [
                                   "ISBN: 393045218",
                                   "Title: The Mummies of Urumchi",
                                   "Author: E. J. W. Barber",
                                   "Publisher: W. W. Norton &amp; Company"
                                   "Year: 1999"
                                   ]
                                 ]
            }
    }

    and an example after an ISBN search:

    {
        (("393045",), SearchType.ISBN):
            {
             SearchInfo.MATCHED_WORDS:["393045218"],
             SearchInfo.RESULTS:["393045218"], 
             SearchInfo.MATCHED_BOOK_INFO:[
                                  [
                                   "ISBN: 393045218",
                                   "Title: The Mummies of Urumchi",
                                   "Author: E. J. W. Barber",
                                   "Publisher: W. W. Norton &amp; Company"
                                   "Year: 1999"
                                   ]
                                 ]
            }
    }

    The use_gui property was added when the declaration of font types caused issues
    in unit testing. It is set to False when using a presenter object within a unit 
    test.

    The font and boldfont properties are used to format the text widgets that are
    displayed in the book search results frame. The boldfont is used to emphasise
    strings that have been a match to the search term.

    A presenter is created when a new book search window is opened. It is initialised
    in the function where the book search window determines what type of search needs
    to be performed and a reference to it is passed on to the relevant search function.
    Results and matched strings are added within the search function, and the presenter's
    function to prepare the results (prepare_results_for_presentation) is called as the 
    last instruction of the search function. The function to present the results to the 
    user (results_to_screen) on the screen is called from the book search window.
    """
    def __init__(self, search_info: dict[tuple, dict[str, list[str]]], books: dict[str, dict[str, str]], use_gui=True):
        self.__search_info=search_info
        self.__books=books
        self.__use_gui=use_gui
        if self.__use_gui:
            self.__font=Font(family="Segoe UI", size="12")
            self.__boldfont=Font(family="Segoe UI", size="12", weight="bold")

    @property
    def search_info(self) -> dict[tuple, dict[str, list[str]]]:
        return self.__search_info
    
    @search_info.setter
    def search_info(self, search_info: dict[tuple, dict[str, list[str]]]) -> None:
        self.__search_info=search_info

    @property
    def books(self) -> dict[str, dict[str,str]]:
        return self.__books
    
    @books.setter
    def books(self, books: dict[str, dict[str, str]]) -> None:
        self.__books=books

    @property
    def use_gui(self) -> bool:
        return self.__use_gui
    
    @use_gui.setter
    def use_gui(self, use_gui: bool) -> None:
        self.__use_gui=use_gui

    @property
    def matched_book_info(self) -> list[list[str]]:
        return self.__matched_book_info
    
    @matched_book_info.setter
    def matched_book_info(self, matched_book_info: list[list[str]]) -> None:
        self.__matched_book_info=matched_book_info

    @property
    def font(self) -> Font:
        return self.__font
    
    @font.setter
    def font(self, font: font) -> None:
        self.__font=font

    @property
    def boldfont(self) -> Font:
        return self.__boldfont
    
    @boldfont.setter
    def font(self, boldfont: font) -> None:
        self.__boldfont=boldfont

    """
    Find the string to be highlighted within the book info and set the font of that string to bold
    """
    def highlight_match(self, text_widget: Text, term: str, tag_name: str) -> None:
        start = "1.0" # start at the first character of the first line
        while True:
            start = text_widget.search(term, start, END, nocase=True) # determine start index of match
            if not start:
                break
            end = text_widget.index(f"{start}+{len(term)}c") # calculate end index of match
            text_widget.tag_add(tag_name, start, end) # apply bold tag 
            start = end # move to the next string
    """
    Create and configure text widgets that will hold the book information

    Add book info to text widget, highlight the matched strings within the text
    and add it to the frame to appear on the screen
    """
    def init_result_text(self, frame: Frame, result_text: list[str], search_info_key: tuple[tuple[str], SearchType] ) -> None:
      
        text_widget = Text(frame, height=7, width=80, font=self.__font, wrap=WORD)   
        text_widget.tag_config("bold", font=self.__boldfont)
        
        for line in result_text:
            text_widget.insert(END, line + "\n")

        terms_to_highlight=self.__search_info[search_info_key][SearchInfo.MATCHED_STRINGS]
        for term in terms_to_highlight:
            self.highlight_match(text_widget, term, "bold")

        text_widget.pack(padx=(20,0), pady=10) 

    """
    Take the results from the search function and prepare the book info to be added to the text widgets 
    """
    def prepare_results_for_presentation(self, search_info_key: tuple[tuple[str], SearchType] ) -> None:
        isbns=self.__search_info.get(search_info_key).get(SearchInfo.RESULTS)
        self.__search_info[search_info_key].setdefault(SearchInfo.MATCHED_BOOK_INFO, list())
        if isbns:
            for isbn in isbns:
                book_to_add=[]
                book_to_add.append("ISBN: " + isbn)
                for k, v in self.books[isbn].items():
                    book_to_add.append(k + ": " + v)
                
                self.__search_info[search_info_key][SearchInfo.MATCHED_BOOK_INFO].append(book_to_add)
    """
    Take prepared book info and call function to add it to screen
    """
    def results_to_screen(self, frame: Frame, search_info_key: tuple[tuple[str], SearchType]) -> None:
        matched_book_info=self.__search_info[search_info_key][SearchInfo.MATCHED_BOOK_INFO]
        no_book=[Result.NO_BOOK]
        if not matched_book_info:
            self.__search_info[search_info_key][SearchInfo.MATCHED_BOOK_INFO].append(no_book) # store for future display
            self.init_result_text(frame, no_book, search_info_key)
        else:
            for book in matched_book_info:
                self.init_result_text(frame, book, search_info_key)
