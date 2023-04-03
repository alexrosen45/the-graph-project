"""CSC 111 Final Project: File Dialog

Module Description
==================
This file contains our FileDialog classs, used to prompt the user which
file they want to load or save. It is accessible by pressing l or s.

Copyright Information
=====================
This file is licensed under the MIT License
"""
import tkinter
import tkinter.filedialog
from typing import IO


class FileDialog:
    """
    It turns out to make a file dialog we need to use tkinger...
    This was a painful learning process to get the file dialog to work on macOS
    in combination with pygame. In particular, this tkinter class needs
    to be initialized really early.

    Instance Attributes:
    - top: an invisible Tk window to make a dialog from
    """
    top: tkinter.Tk

    def __init__(self) -> None:
        self.top = tkinter.Tk()
        self.top.withdraw()

    def prompt_file(self) -> str:
        """Create a Tk file dialog and cleanup when finished
        If the specified file is not in CSV format, return an empty string"""
        file_name = tkinter.filedialog.askopenfilename(parent=self.top, filetypes=[("CSV", "*.csv")])
        self.top.withdraw()  # hide window
        return file_name

    def ask_file(self) -> (IO | None):
        """Create another Tk file dialog and cleanup when finished"""
        file_name = tkinter.filedialog.asksaveasfile(parent=self.top)
        self.top.withdraw()  # hide window
        return file_name


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(
        config={
            "extra-imports": ["tkinter", "tkinter.filedialog", "typing"],
            "allowed-io": [],
            "max-line-length": 100,
        }
    )
