import os
from md_file import MD_file
from utils import *
import tkinter as tk
import tkinter.ttk as ttk
from GUI import GUI


def main():
    """
    Function which starts the main program loop
    """
    # choose a working directory
    working_dir = get_working_dir()

    if not type(working_dir) is str:
        exit()

    # create the list with all file paths
    data_file_list = create_data_file_list(working_dir)

    # load the list filled with keywords
    keywords = load_keywords()
    print(keywords)

    # create the MD_file_dict
    MD_files = create_MD_file_dict(data_file_list, keywords)
    
    # create the gui object
    gui_handler = GUI(working_dir, MD_files, keywords)
    # start the mainloop
    gui_handler.start_mainloop()
    

    





# execute main if main.py is run
if __name__ == "__main__":
    main()