from tkinter import *
from tkinter import ttk
import graph_data
import graph_matrix
from PIL import Image, ImageTk
from constants import GraphPhotoPath, GraphList

class GraphWindow(Toplevel):
    def __init__(self):
        super().__init__()

        self.graphs=[member for member in GraphPhotoPath]
        self.selected_graph_name=""
        self.selection_frame=Frame(self)
        self.selection_frame.grid(row=0, column=0)

        self.instruction_label=Label(self.selection_frame, text="Please select a graph to display its adjacency matrix an visual representation: ")
        self.instruction_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        self.graphs_combobox=ttk.Combobox(self.selection_frame, values=[str(member) for member in GraphPhotoPath]) 
        self.graphs_combobox.bind("<<ComboboxSelected>>", self.update_matrix)
        self.graphs_combobox.grid(row=1, column=0, columnspan=2, padx=20, pady=2)

        self.matrix_frame=Frame(self)
        self.matrix_frame.grid(row=1, column=0, padx=10, pady=10)

        # Create a canvas for the image
        self.canvas = Canvas(self)
        self.canvas.grid(row=2, column=0, pady=(0,20), padx=20)

        # Create a placeholder image on the canvas
        tk_image = None
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=tk_image)
    
    """
    Display the adjacency matrix of the selected graph

    Clear any existing labels from the grid. Gets the selected graph name
    from the combobox and uses the name to access the graph from the dictionary
    of graphs. Creates and initalises a matrix based on the graph and populates it.
    Calls methods to dipslay the matrix and adjust window size.
    """

    def update_matrix(self, e: Event) -> None:
        self.swap_matrix_frame()
        self.selected_graph_name=self.graphs_combobox.get()
        graph=graph_data.graphs[self.selected_graph_name]
        matrix=graph_matrix.init_matrix(graph)
        graph_matrix.populate_matrix(matrix, graph)
        self.display_matrix(matrix)
        self.display_visual(self.selected_graph_name)
        

    """
    Destroy frame holding the matrix and create new frame

    Needed to allow automatic window resizing when switching from
    one adjacency matrix to another.
    """
    def swap_matrix_frame(self) -> None:
        self.matrix_frame.destroy()
        self.matrix_frame=Frame(self)
        self.matrix_frame.grid(row=1, column=0, padx=20, pady=20)

    """
    Display label widgets for each value of a 2-dimensional list (matrix)

    Takes the adjacency matrix of the selected graph and displays it as a grid of labels. 
    The grid lines comprise of the borders of the label widgets.Rows and columns of the grid 
    are configured to take up the same size as each other and resize with the window. 
    """
    def display_matrix(self, matrix: list) -> None:
        for x in range(len(matrix)):
            for y in range(len(matrix)):
                label=Label(self.matrix_frame, text=matrix[x][y], relief="solid", borderwidth=1, font="bold", padx=10, pady=10)
                label.grid(row=x, column=y,sticky=NSEW)
                self.labelwidth=label.winfo_width()
                self.labelheight=label.winfo_height()
                self.matrix_frame.grid_rowconfigure(x, weight=1, uniform="uniform_size")
                self.matrix_frame.grid_columnconfigure(y, weight=1, uniform="uniform_size")
     
        self.framewidth=self.labelwidth * len(matrix)
        self.frameheight=self.labelheight * len(matrix[0])
        self.matrix_frame.config(height=self.frameheight, width=self.framewidth)
        graph_label=Label(self.matrix_frame, text=GraphList[self.selected_graph_name.upper()].value, justify=RIGHT)
        graph_label.grid(row=0, column=len(matrix)+1, rowspan=len(matrix[0]), padx=10, pady=10)
        self.matrix_frame.update_idletasks()

        

    """
    Display the visual graph representation

    Retrieve image path from the graph Enum and open an image with Pillow,
    then convert that image for Tkinter. Update the already existing canvas to match
    the size of the image and update the image on the canvas to the newly selected
    graph visual image.
    """
    def display_visual(self, graph_name: str) -> None:
        graph_name=graph_name.upper()
        self.img_path=GraphPhotoPath[graph_name].value
        self.image = Image.open(self.img_path) 
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.config(width=self.image.width, height=self.image.height)
        self.canvas.itemconfig(self.image_on_canvas, image=self.tk_image)
                    


        
