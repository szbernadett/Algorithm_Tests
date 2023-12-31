from tkinter import font
from main_window import MainWindow



if(__name__=="__main__"):
    main_window=MainWindow()
    default_font = font.nametofont("TkDefaultFont")
    default_font.config(size=11)
    main_window.mainloop()