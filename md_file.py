import os

class MD_file:
    """
    Class to handle all the metadata 

    Idea:
        - creating a class to use like a typical dictionary
        - saving and loading data to and from the disc
    """
    def __init__(self, path, keywords):
        """
        Initialization of the file handler object

            path     - string   ... path to the data file
            keywords - list     ... list of all metadata keywords
        """
        # setting the path of the data file
        self.path = path
        # creating the path to the metadata
        self.metadata_path = os.path.join(os.path.split(path)[0], "metadata", 
                                          os.path.split(path)[1].replace(".", "-") + "-metadata.txt")

        # saving the keywords
        # each md file needs its own copy
        self.keywords = list(keywords)

        # checking if the metadata directory is initialized
        if not os.path.isdir(os.path.join(os.path.split(self.path)[0], "metadata")):
            os.makedirs(os.path.join(os.path.split(self.path)[0], "metadata"))
        
        # intializing the data dict
        self.data = {}
        for key in self.keywords:
            self.data[key] = ""

        # checking if the metadata file is initialized
        if not os.path.isfile(self.metadata_path):
            # writing the init data dict
            self.write()

        # loading data if available
        self.read()


    def read(self):
        """
        Function to load metadata if available from the file
        """
        # opening the file 
        with open(self.metadata_path, 'r') as tmp:
            # reading all lines skipping over reference to original file
            md = tmp.readlines()
            # check if the second line is empty
            if md[1] == "\n":
                md = md[2:]
            else:
                md = md[1:]

        # parsing the actual data
        for line in md:
            # getting the key and the data
            key, info = line.split(":  ")

            # writing the data into our data dict
            self.data[key] = info.replace("\n", "")

    
    def create_save_string(self):
        """
        Function to create the save string

        return:
            save_string - string ... string that contains the data dict
        """
        # initializing the empty string
        save_string = ""

        # adding the reference to the data file
        save_string += "path to data file: " + self.path + "\n" + "\n"

        # iterate over the data dict
        for key in self.keywords:
            # adding the key, info pair to the save_string
            save_string += key + ":  " + self.data[key] + "\n"
        
        # returning the created string
        return save_string


    def write(self):
        """
        Function to write the metadata to the file
        """
        # creating the save string composed of the metadata in self.data
        save_string = self.create_save_string()

        # opening the file
        with open(self.metadata_path, "w+") as file:
            # writing the save_string
            file.write(save_string)


    def set_keywords(self, keywords):
        """
        Setter Function to update the keyword lists
        
            keywords - list     ... list of all metadata keywords
        """
        self.keywords = keywords

        # add an empty string for new keywords
        for key in self.keywords:
            if not key in self.data:
                self.data[key] = ""

    def update_keyword(self, i, keyword):
        """
        function to update a single keyword (index i)

            i       - index  ... index of the keyword you want to update
            keyword - string ... new keyword for index i
        """
        self.data[keyword] = self.data[self.keywords[i]]
        self.keywords[i] = keyword

    def __getitem__(self, key):
        """
        Operator overloading to simplify usage of the class
        """
        return self.data[key]


    def __setitem__(self, key, value):
        """
        Operator overloading to simplify usage of the class
        """
        self.data[key] = value.replace("\n", "")
        # also overwrite the metadata file
        self.write()

    def __str__(self):
        """
        Defines a string representation for the class so that its printable
        """ 
        return str(self.data)