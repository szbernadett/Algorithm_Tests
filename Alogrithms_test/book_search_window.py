from tkinter import *
from tkinter import ttk
import new_search_util
import book_data
from presenter import Presenter
from constants import *
from tkinter import messagebox

class BookSearchWindow(Toplevel):
    def __init__(self):
        super().__init__()
        self.presenter=Presenter(dict(), book_data.books)
        self.search_info_key=None   

        ###########################################################################
        #                             BOOK SEARCH FRAME                           #
        ###########################################################################

        # SEARCH FRAME 
        self.book_search_frame = ttk.LabelFrame(self, text="Book Search") 
        self.book_search_frame.pack(side=TOP, fill=BOTH, expand=False, padx=40, pady=(40, 10))
        self.style=ttk.Style(self)
        self.style.configure("TEntry", padding="7")

        # INSTRUCTIONS FRAME WITH SEARCH INSTRUCTIONS
        self.instructions_frame=ttk.Frame(self.book_search_frame)
        self.instructions_frame.pack(side=TOP, fill=X, pady=(40, 30))
        self.search_instructions = (
                                "Search for title, author or publisher: enter the full information or an identifying part avoiding single letters and common words (and, or, the, etc.)\n"
                                "\n"
                                "Search by year: enter all four digits, e.g. 2002. Ranges (2002-2005, <2001 etc.) are not allowed.\n"
                                "\n"
                                "Search by ISBN: enter between 5-13 characters, if it is less or more than that, search is not performed\n"
                                "\n"
                                "Excess whitespace, special characters, punctuation, single letter and common words are automatically removed\n"                                
                                "\n"
                                "If the entered term doesn't contain qualifying information, no search is performed"
                            )
        self.search_instructions_label = ttk.Label(self.instructions_frame, text=self.search_instructions, wraplength=800)
        self.search_instructions_label.pack(side=LEFT, padx=20, pady=20)

        # SEARCH FRAME WITH SEARCH BAR AND SEARCH BUTTON
        self.search_bar_frame=ttk.Frame(self.book_search_frame) 
        self.search_bar_frame.pack(side=TOP, fill=X) 
        self.search_bar = ttk.Entry(self.search_bar_frame, style="TEntry", width=100) # SEARCH BAR
        self.search_bar.pack(side=LEFT, padx=(20,10), pady=5)
        self.search_button = ttk.Button(self.search_bar_frame, text="Search", command=self.search_button_pressed) # SEARCH BUTTON
        self.search_button.pack(side=LEFT, padx=(10, 20), pady=20)

        # RADIO FRAME WITH TWO RADIO BUTTONS 
        self.radio_frame=ttk.Frame(self.book_search_frame) 
        self.radio_frame.pack(side=TOP, fill=X) 
        self.search_options_label = ttk.Label(self.radio_frame, text="When searching for title, author or publisher, use: ")
        self.search_options_label.pack(side=LEFT, padx=20, pady=10)

        self.word_search_method = StringVar(value=SearchType.LEVENSHTEIN) # variable that holds the selected method

        # Radio buttons for choosing search method
        self.radio_in = ttk.Radiobutton(self.radio_frame, text="'in' operator", variable=self.word_search_method, value=SearchType.IN)
        self.radio_levenshtein = ttk.Radiobutton(self.radio_frame, text="Levenshtein distance", variable=self.word_search_method, value=SearchType.LEVENSHTEIN)

        self.radio_in.pack(side=LEFT, padx=5, pady=10)
        self.radio_levenshtein.pack(side=LEFT, padx=5, pady=10)

        ###########################################################################
        #                            RESULTS FRAME                                #
        ###########################################################################

        # RESULTS FRAME 
        self.results_frame = ttk.LabelFrame(self, text="Results")
        self.results_frame.pack(side=TOP, fill=BOTH, expand=True, padx=40, pady=(0,40))

        # CANVAS
        self.canvas = Canvas(self.results_frame)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # SCROLLBAR ADDED TO CANVAS
        self.yscrollbar = Scrollbar(self.results_frame, orient=VERTICAL, command=self.canvas.yview)
        self.yscrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.configure(yscrollcommand=self.yscrollbar.set)

        # ADD INNER FRAME TO CANVAS
        self.inner_frame = Frame(self.canvas)
        self.inner_frame.bind("<Configure>", self.on_configure)
        self.canvas_window=self.canvas.create_window((0, 0), window=self.inner_frame, anchor=NW)


    def on_configure(self, e: Event) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.itemconfig(self.canvas_window, width=self.canvas.winfo_width())

    def on_canvas_configure(self, event: Event) -> None:
        # Set the width of the inner_frame to the current width of the canvas
        self.canvas.itemconfig("inner_frame", width=event.width)
    
    """
    Retrieve string from search bar, remove unwanted characters and
    white space, split it into separate words and return it in a list
    """
    def get_search_terms(self) -> list[str]:
        raw_string=self.search_bar.get()
        cleaned_strings=new_search_util.prepare_string(raw_string)
        return cleaned_strings
    
    """
    Perform search and present results

    Get the prepared search terms. Call the function that determines which
    search to perform. Call the function that perfomrs the search based on
    search type and returns the results. Call the presenter's function to 
    make the results appear on the screen. Update GUI.
    """
    def search_button_pressed(self) -> None:
        terms=self.get_search_terms() 
        search_type=new_search_util.select_search_type(terms)
        self.get_results(search_type, terms)

        for child in self.inner_frame.winfo_children():
            if isinstance(child, Text):
                child.destroy()

        self.presenter.results_to_screen(self.inner_frame, self.search_info_key)
        self.update()
    
    """
    Perform search based on search type or if search type undetermined, present
    an error message to the user

    Examine serch type, initialise presenter and call appropriate function to perform
    search that matches the search type. Search results are held by presenter object
    and added within the specific search function called. 
    """

    def get_results(self, search_type: SearchType, terms: list[str]) -> None:
        if search_type != SearchType.UNDETERMINED:
            match search_type:
                case SearchType.YEAR:
                    self.search_info_key=(tuple(terms), SearchType.YEAR)
                    self.presenter.search_info.setdefault(self.search_info_key, dict())
                    if self.presenter.search_info.get(self.search_info_key).get(SearchInfo.RESULTS) is None:
                        new_search_util.year_search(book_data.year_index, terms[0], self.presenter, self.search_info_key)
                case SearchType.ISBN:
                    self.search_info_key=(tuple(terms), SearchType.ISBN)
                    self.presenter.search_info.setdefault(self.search_info_key, dict())
                    if self.presenter.search_info.get(self.search_info_key).get(SearchInfo.RESULTS) is None:
                        new_search_util.isbn_search(self.presenter, self.search_info_key, terms[0])
                case SearchType.WORD:
                    method=self.word_search_method.get()
                    search_source=list(book_data.title_author_publisher_index.keys())
                    search_source.sort(key=len) 
                    match method:
                        case SearchType.LEVENSHTEIN:
                            self.search_info_key=(tuple(terms), SearchType.LEVENSHTEIN)
                            self.presenter.search_info.setdefault(self.search_info_key, dict())           
                            if self.presenter.search_info.get(self.search_info_key).get(SearchInfo.RESULTS) is None:
                                new_search_util.search_all_with_levenshtein_distance(book_data.title_author_publisher_index, search_source, self.presenter, self.search_info_key)
                        case SearchType.IN:
                            self.search_info_key=(tuple(terms), SearchType.IN)
                            self.presenter.search_info.setdefault(self.search_info_key, dict())
                            if self.presenter.search_info.get(self.search_info_key).get(SearchInfo.RESULTS) is None:
                                new_search_util.search_all_with_in_operator(book_data.title_author_publisher_index, search_source, self.presenter, self.search_info_key)
        else:
            messagebox.showerror("Input Error", "Please enter a valid search term", parent=self)
        
