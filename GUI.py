import os
from md_file import MD_file
from utils import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


class GUI:
    """
    Class to handle the GUI elements.
    this includes:
        - a treeview as a file browser
        - a list of editable metadata entries
        - buttons to edit the processing steps
        - buttons for fast process options
        - buttons to add and remove keywords
    """
    def __init__(self, working_dir, MD_files, keywords):
        """
        Initializes the GUI handler

            working_dir     - string    ... path to the working directory
            MD_files        - dict      ... dict containing MD_file dict wrapper for the metadata files
            keywords        - list      ... list containing all metadata keywords 
        """
        # saving important parameters
        self.working_dir = working_dir
        self.MD_files = MD_files
        self.keywords = keywords

        # creating the tk master window
        self.master = tk.Tk()
        self.master.title("Metadata Tool")

        # creating a frame for the treeview
        self.tree_frame = tk.Frame(self.master)

        # fixing the geometry so that the window is resizable
        self.tree_frame.grid(column=0, row=0, sticky="nsew", padx = 10, pady = 10)
        self.master.rowconfigure(0, weight=1)

        # creating the treeview object which is used to display the files in working_dir
        # using selectmode browse disables multiple selections in the treeview
        self.tree = ttk.Treeview(self.tree_frame, selectmode="browse")
        self.tree.heading("#0" ,text="File List")
        self.tree.grid(column=0, row=1, sticky="ns")
        self.tree_frame.rowconfigure(1, weight=1)

        # loading the logo (as a gif because tkinter)
        # and displaying the logo abouth the tree view
        self.logo_canvas = tk.Canvas(self.tree_frame, width=200, height=64)
        self.logo = tk.PhotoImage(master=self.logo_canvas, file="saldilogo.gif")
        self.logo_canvas.create_image((0,0), image=self.logo, anchor="nw")
        self.logo_canvas.grid(column=0, row=0, sticky="nw", pady=5)

        # filling the treeview object
        self.root = self.tree.insert("", "end", text=os.path.relpath(self.working_dir, os.getcwd()), open=True)
        self.create_treeview(self.working_dir, self.root)

        # binding the tree select event to the treeview object to open the selected metadata file
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_selection)

        # topframe is needed to create the list of entries later on
        self.topframe = None


    def create_treeview(self, path, parent):   
        """
        Recursive function which adds an tree element for each data file in the given path

            path    - string        ... path to the directory which should be processed
            parent  - tree element  ... the parent element of this directory
        """ 
        # iterate over all elements in path
        for p in os.listdir(path):
            # concatenate the path and p
            abspath = os.path.join(path, p)
            # checking if its not a metadata directory
            if not "metadata" == p:
                #insert the element into the treeview
                parent_element = self.tree.insert(parent, "end", text=p, open=True)

                # if the added element is a directory 
                if os.path.isdir(abspath):
                    # execute this function with the directory and the directory element as parent
                    self.create_treeview(abspath, parent_element)

    def get_tree_path(self, item):
        """
        Recursive Function to calculate the filepath to a given tree element.

            item    - tree element  ... the element of the tree view for which the path should be created
        returns
            path    - string        ... file path to the tree element
        """
        if self.tree.parent(item) == "":
            return self.tree.item(item)["text"]
        else:
            return os.path.abspath(os.path.join(self.get_tree_path(self.tree.parent(item)), self.tree.item(item)["text"]))

    def frame_focus(self, event):
        """
        Reset the scroll region to encompass the inner frame
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_resize(self, event):
        """
        Function to resize the entry list if the canvas is resized
        """
        padding = 10
        width = self.canvas.winfo_width() - padding
        self.canvas.itemconfigure("entries", width=width)

    def on_return_button(self, event, i):
        """
        function to jump to the next entry box and save the metadata if return is pressed

            i   - index     ... index of the entry in the entry list
        """
        if i < len(self.entry_list)-1: # exclude the last entry
            self.entry_list[i+1].focus_set()

        # get the path to the data file
        path = os.path.join(self.working_dir, self.file_name.get())
        # save the metadata of the entry box
        self.MD_files[path][self.keywords[i]] = self.stringvar_list[i].get()

    def on_up_button(self, event, i):
        """
        function to jump to the previous entry box and save the metadata if the up arrow is pressed

            i   - index     ... index of the entry in the entry list
        """
        if i > 0: # exclude the first entry
            self.entry_list[i-1].focus_set()

        # get the path to the data file
        path = os.path.join(self.working_dir, self.file_name.get())
        # save the metadata of the entry box
        self.MD_files[path][self.keywords[i]] = self.stringvar_list[i].get()

    def on_entry_focus_loss(self, event, i):
        """
        function to save the metadata if an entry looses focus

            i   - index     ... index of the entry in the entry list
        """
        # get the path to the data file
        path = os.path.join(self.working_dir, self.file_name.get())
        # save the metadata of the entry box
        self.MD_files[path][self.keywords[i]] = self.stringvar_list[i].get()

    def on_ctrl_s(self, event):
        """
        Function to save the current metadata if ctrl + s are pressed
        """
        # save the metadata
        self.save_current_metadata()
        # set focus to the master window
        # this indicates to the user that something happened
        self.master.focus_set()

    def on_tree_selection(self, event):
        """
        Function which handles the tree selection element
        inspired by:
            https://stackoverflow.com/questions/34849035/how-to-get-the-value-of-a-selected-treeview-item
        """
        # first identify the selected tree element
        #element = self.tree.identify('item',event.x,event.y)
        element = self.tree.selection()[0]
        # second get the path of this tree element
        path = self.get_tree_path(element)

        # check if the path is a directory (only files should be opened)
        if os.path.isdir(path):
            return

        # control output
        print("changed to file: ", path)
        # this bool determines if the metadata should be saved if the file is changed
        save_md = True

        # check if the entry list was already created
        # this is needed to set the focus on the first double clicked file
        if self.topframe is None:
            self.create_entry_list()
            # do not save empty strings if this is the first opened file
            save_md = False

        # if we want to save the metadata 
        # (everytime except the first time we click on a data file because then the entry variables are empty)
        if save_md:
            # save the path of the closed data file in a temp variable to save the meta data
            old_path = os.path.join(self.working_dir, self.file_name.get())
        
        # set the filename label to the newly opened file
        self.file_name.set(os.path.relpath(path, self.working_dir))

        # iterate over the keywords and load the metadata from the corresponding file
        # save the metadata of the closed file to the disc
        # (everytime except the first time we click on a data file because then the entry variables are empty)
        for i,keyword in enumerate(self.keywords):
            if save_md:
                self.MD_files[old_path][keyword] = self.stringvar_list[i].get()
            self.stringvar_list[i].set(self.MD_files[path][keyword])

    def save_current_metadata(self):
        """
        Function which saves the metadata for the currently opened file
        """
        # if a file was opened
        if not self.topframe is None:
            # create the path
            path = os.path.join(self.working_dir, self.file_name.get())

            # save each entry
            for i,keyword in enumerate(self.keywords):
                self.MD_files[path][keyword] = self.stringvar_list[i].get()

    def create_entry_list(self):
        """
        Function to create a scrollable resizable list of tkinter widgets
        """
        # to get a scrollable list of tkinter widgets which are resizable the following steps are needed:
        # 1. create a top frame
        #       this frame will hold the canvas and scrollbar so that they are the same size and can be displayed on the grid
        self.topframe = tk.Frame(self.master)
        # 2. set sticky to all 4 directions and the weight to >0 that the frame can be resized if the window dimensions change  
        self.topframe.grid(column=1, row=0, sticky="nsew", padx = 10, pady = 10)
        self.master.columnconfigure(1, weight=4)

        # 3. create the canvas and the scrollbar in the top frame 
        self.canvas = tk.Canvas(self.topframe)
        self.scrollbar = tk.Scrollbar(self.topframe, orient="vertical", command=self.canvas.yview)
        # 4. add the scrollbar to the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # 5. create the frame for the widgets on the canvas
        self.entry_frame = tk.Frame(self.canvas)
        
        # 6. grid the scrollbar and the canvas
        self.scrollbar.grid(row=0,column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        # 7. set the weights for the canvas and scrollbar so that they are resizable
        self.topframe.rowconfigure(0, weight=4)
        self.topframe.columnconfigure(0, weight=4)

        # 8. blit the widget frame onto the canvas
        self.canvas.create_window((0,0),window=self.entry_frame,anchor="nw", tags=["entries"])
        
        # 9. bind a function to the widget frame that it stays in focus and cant be scrolled away
        self.entry_frame.bind("<Configure>", self.frame_focus)
        # 10. bind a function to the canvas which updates the width of the widget frame if the window is resized 
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # setting the weigth of the entries to 1 so that they stretch if the window is resized
        self.entry_frame.columnconfigure(1, weight=1)

        self.label_list = []
        self.entry_list = []
        self.stringvar_list = []

        # 11. finally add the planned widgets on the widget frame
        self.file_name = tk.StringVar(self.master)
        self.entry_list_title = tk.Label(self.entry_frame, font = "Courier 18", textvariable=self.file_name)
        self.entry_list_title.grid(row=0, columnspan=2, sticky="ew", pady=3, padx=15)
        for i,keyword in enumerate(self.keywords):
            self.label_list.append(tk.Label(self.entry_frame, font = "Courier 12", text=keyword).grid(row=i+1,column=0, sticky="w", pady=1, padx=4))

            self.stringvar_list.append(tk.StringVar(self.master))
            self.entry_list.append(tk.Entry(self.entry_frame, font = "Courier 12", textvariable=self.stringvar_list[-1]))
            self.entry_list[-1].grid(row=i+1, column=1, sticky="ew", pady=1)
            
            # bind the on return function
            # 1. create a lambda to get a new scope where our i is not overwritten
            #    see also https://stackoverflow.com/questions/14259072/tkinter-bind-function-with-variable-in-a-loop
            def create_return_lambda(j):
                return lambda event: self.on_return_button(event, j)
            
            # 2. bind the created lambda
            self.entry_list[-1].bind('<Return>', create_return_lambda(i))

            # doing the same for up and down arrow keys
            # down arrow key gets the same functionality as return
            # we can therefore reuse our functions
            self.entry_list[-1].bind('<Down>', create_return_lambda(i))

            # up arrow needs a similar functionality
            def create_up_lambda(j):
                return lambda event: self.on_up_button(event, j)

            self.entry_list[-1].bind('<Up>', create_up_lambda(i))

            # bind focus out event to save the metadata 
            # this double saves in case of enter, up or down but is mainly if the mouse clicks on something different
            # this is mainly a safety measure to minimize data loss
            def create_focus_loss_lambda(j):
                return lambda event: self.on_entry_focus_loss(event, j)

            self.entry_list[-1].bind('<FocusOut>', create_focus_loss_lambda(i))

        # bind ctrl + s to the master window to save the metadata and loose focus of the current entry
        # this is only done now to make sure the entries already excist
        self.master.bind('<Control-s>', self.on_ctrl_s)

    def on_closing(self):
        """
        Function which saves the open metadata and destroys the master window
        """
        # save the currently opened file
        self.save_current_metadata()

        if messagebox.askokcancel("Quit", "Do you want to quit?\nProgress will be saved."):
            # these both calls fix the issue with linux and not closing properly
            self.master.quit()
            self.master.destroy()

    def start_mainloop(self):
        """
        Function which starts the tkinter main loop
        and handles exit behaviour of the main loop
        """
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.mainloop()