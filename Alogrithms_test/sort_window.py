from tkinter import *
from tkinter import ttk
from bubble_sort import bubble_sort
from merge_sort import merge_sort
from timeit import repeat
import book_data
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SortWindow(Toplevel):
    def __init__(self, algorithm_names: list[str]):
        super().__init__()

        # THREAD
        self.test_thread=None
        
        # RESULTS
        self.results=None

        # DESCRIPTION LABEL
        self.description="Press the Test button to run timing tests for a number of algorithms with varying sizes of datasets and display them in a table. When the tests have finished, a chart of the results can be viewed by pressing the Show Chart button."
        self.desc_label=Label(self, text=self.description, anchor=CENTER, justify=LEFT, wraplength=500)
        self.desc_label.grid(row=0, column=0, columnspan=2, sticky=EW, padx=40, pady=(40,20))

        # TEST BUTTON
        self.test_button=Button(self, text="Start Test", command=self.start_test_thread) # start thread
        self.test_button.grid(row=1, column=0, padx=20, pady=20)

        # PLOT BUTTON
        self.plot_button=Button(self, text="Show Chart", command=lambda: self.plot_results(self.results))
        self.plot_button.grid(row=1, column=1, padx=20, pady=20)
        self.plot_button.config(state=DISABLED)

        # PROGRESS BAR
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=200, mode="indeterminate")
        self.progress_bar.grid(row=2, column=0, padx=10, pady=20)

        self.progress_bar_label = Label(self, text="", anchor=W)
        self.progress_bar_label.grid(row=2, column=1, pady=20, sticky=W)

        # DATASETS TO SORT
        self.algorithm_names=algorithm_names
        self.titles_10k=book_data.get_book_titles_from_csv("10kbooks.csv")
        
        self.titles_1000=self.titles_10k[:1000]
        self.titles_100=self.titles_10k[:100]
        self.titles_10=self.titles_10k[:10]
        self.all_titles=[self.titles_10, self.titles_100, self.titles_1000, self.titles_10k]

        # CREATE TREEVIEW
        self.results_tree = ttk.Treeview(self)

        # COLUMNS
        self.col_names=["algorithm_"+str(i+1) for i in range(len(self.algorithm_names))]
             
        self.results_tree["columns"] = ("dataset_size", *self.col_names)
        self.results_tree.column("#0", width=0, stretch=NO)  #  ID columns
        self.results_tree.column("dataset_size", anchor=W, width=120)

        self.results_tree.heading("dataset_size", text="Dataset Size", anchor=W)

        for j in range(len(self.col_names)):
            col_name, col_header=self.col_names[j-1], self.algorithm_names[j-1]
            self.results_tree.column(col_name, anchor=W, width=150)
            self.results_tree.heading(col_name, text=col_header,anchor=CENTER)
    
        self.results_tree.grid(row=3, column=0, columnspan=2, padx=20, pady=(0,20))

    """
    Create thread to run sort timing task

    Create thread that comes alive when 'Test' button is pressed. Run the
    function that runds, updates and stops the progress bar.
    """
    ######################################################################
    #                      THREAD AND PROGRESS BAR                       #
    ######################################################################

    def start_test_thread(self):
        self.test_thread = threading.Thread(target=self.test_button_pressed, daemon=True) # triggered by test button
        self.test_thread.start()
        self.update_progress_bar()

    """
    Start, update and stop the progress bar
    
    Check that the thread that needs the progress bar to show it is working
    is still alive. If alive, start progress bar. The self.after function
    creates a loop that checks the status of the parent thread every 100 milli-
    seconds, and if the thread is dead, move exectuion to the 'else' branch
    where progress bar is stopped.
    """
    def update_progress_bar(self):
        if self.test_thread.is_alive():
            self.progress_bar.start(10)  # Start the progress bar animation
            self.progress_bar_label.config(text="Running tests...") # Show text in label
            self.after(100, self.update_progress_bar)  # Check again after 100ms
        else:
            self.progress_bar.stop()  # Stop the progress bar when the thread finishes
            self.progress_bar_label.config(text="")
    
    """
    Run the sorting algorithm on a given dataset multiple times and return 
    the execution times from each execution

    The setup argument should contain the information that tells the function where
    to find the algorithms, or in other words, which modules to import them from.
    One timing process executes the statement (the sorting algorithm with a given
    dataset) 5 times (number) and the whole timing process is repeated 3 times and
    the corresponding times are returned in a list.
    """

    ######################################################################
    #                      TIMING TEST FUNCTIONS                         #
    ######################################################################

    def time_sort_test(self, algorithm_name: str, dataset: list[str]) -> list[float]:
        setup=f"from {algorithm_name} import {algorithm_name}"
        statement=f"{algorithm_name}({dataset})"
        times=repeat(setup=setup, stmt=statement, repeat=3, number=5)

        return times
    
    """
    Run the sort timing function on one or more algorithm in a 
    collection and gather their time results in a dictionary

    Repeat the timing test on each algorithm with all avaliable datasets,
    register results in 
    """
    
    def time_all(self) -> dict[str, list[float]]:
        
        res=dict()
        for algorithm_name in self.algorithm_names:
            for dataset in self.all_titles:
                time=min(self.time_sort_test(algorithm_name, dataset))
                res.setdefault(algorithm_name, list()).append(time)

        return res
    
    ######################################################################
    #                   TEST AND PLOT BUTTON FUNCTIONS                   #
    ######################################################################
    
    """
    Call function to perform timing tests and when those have finished,
    update the user interface
    """
    def test_button_pressed(self) -> None:
        self.results=self.time_all()
        self.after(0, self.update_ui)

        
    """
    Populate treeview with results and toggle button states
    """
    def update_ui(self) -> None:
        if not self.results:
            return
        
        count=0
        for x, title in enumerate(self.all_titles):
            row_data=[len(title)] + [self.results[algo][x] for algo in self.algorithm_names]
            self.results_tree.insert(parent="", index=END, iid=count, text="", values=row_data)
            count+=1
        
        self.plot_button.config(state=NORMAL)
        self.test_button.config(state=DISABLED)

    """
    Create chart from timing test results and add present it in the window
    """
    def plot_results(self, test_results: dict[str, list[float]]) -> None:
        
        elements = [10, 100, 1000, 10000]
        times_1 = test_results[self.algorithm_names[0]]
        times_2 = test_results[self.algorithm_names[1]]


        # Create the Matplotlib figure and axes
        fgr, ax = plt.subplots()
        ax.plot(elements, times_1, marker="o", color="blue", label=self.algorithm_names[0])
        ax.plot(elements, times_2, marker="x", color="red", label=self.algorithm_names[1])
        ax.set_title("Execution Time by Number of Elements")
        ax.set_xlabel("Number of Elements")
        ax.set_ylabel("Execution Time (seconds)")
        ax.legend()
        
        canvas = FigureCanvasTkAgg(fgr, master=self)  # Create a tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=20, pady=20)  # Add canvas to Tkinter grid

        self.plot_button.config(state=DISABLED)

   
