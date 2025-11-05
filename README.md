# file-compare-customtkinter

Simple file comarison GUI application that relies on `difflib`.

Created to remind self how to do things with tkinter, but using customtkinter which works in a similar way but looks fancier.

Most dependencies can be installed using supplied `requirements.txt` but see **tkinter required** below.


### tkinter required
Although using `customtkinter`, original `tkinter` is required. This **can't** be installed using `pip`, as it's *supposed* to be part of the Python standard library. However, `tkinter` is actually omitted from some common Python installs (e.g. using `brew` or `apt`). In these circumstances, `tkinter` should be installed using the relevant package manager, e.g. `brew install python-tk` or `sudo apt-get install python3-tk`.
 

