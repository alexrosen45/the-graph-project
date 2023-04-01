import tkinter
import tkinter.filedialog

top = tkinter.Tk()
top.withdraw()  # hide window

def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.withdraw()  # hide window
    return file_name

def ask_file():
    file_name = tkinter.filedialog.asksaveasfile(parent=top)
    top.withdraw()  # hide window
    return file_name