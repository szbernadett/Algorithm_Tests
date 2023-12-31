from tkinter import *
from graph_window import GraphWindow
from sort_window import SortWindow
from book_search_window import BookSearchWindow
from constants import SortingAlgorithm

class MainWindow(Tk):

    def __init__(self):
        super().__init__()

        self.title("Algorithm Tests")

        self.graph_frame=LabelFrame(self, text="Graphs")
        self.graph_frame.grid(row=0, column=0, padx=(40, 20), pady=(40, 20), sticky=EW)
        self.graph_label=Label(self.graph_frame, text="View graph representations", padx=10, pady=10)
        self. graph_label.pack()

        self.sort_frame=LabelFrame(self, text="Sorting Algorithms")
        self.sort_frame.grid(row=1, column=0, padx=(40, 20), pady=20, sticky=EW)
        self.sort_label=Label(self.sort_frame, text="Test sorting algorithms", padx=10, pady=10)
        self.sort_label.pack()

        self.book_search_frame=LabelFrame(self, text="Book Search")
        self.book_search_frame.grid(row=2, column=0, padx=(40, 20), pady=(20, 40), sticky=EW)
        self.search_label=Label(self.book_search_frame, text="Search books in a dataset", padx=10, pady=10)
        self.search_label.pack()

        self.graph_button=Button(self, text="Graphs", padx=20, pady=5, 
                               command=lambda: GraphWindow())
        self.graph_button.grid(row=0, column=1, padx=(0, 40), pady=(40, 20), sticky=EW)

        self.sort_button=Button(self, text="Sort", padx=20, pady=5, 
                               command=lambda: SortWindow([alg.value for alg in SortingAlgorithm]))
        self.sort_button.grid(row=1, column=1, padx=(0, 40), pady=20, sticky=EW)

        self.search_button=Button(self, text="Search", padx=20, pady=5, 
                               command=lambda: BookSearchWindow())
        self.search_button.grid(row=2, column=1, padx=(0, 40), pady=(20, 40), sticky=EW)