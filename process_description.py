import os

class PD_handler:
    """
    A class which handels the process descriptions.
    It acts like a dict but is kind of a double dict.

        processes = PD_handler()
        processes.add("Name", "description")

        processes["Name"] # = "description"
        processes[["description"]] # = name
    """
    def __init__(self):
        self.names = {}
        self.descriptions = {}

        self.names["No Description"] = ""
        self.descriptions[""] = "No Description"

    def add(self, name, descr):
        """
        Function to add a description

            name    - string    ... name of the description
            descr   - string    ... description of the process
        """
        self.names[name] = descr
        self.descriptions[descr] = name

    def remove(self, name, descr):
        """
        Function to delete a description

            name    - string    ... name of the description
            descr   - string    ... description of the process
        """
        self.names.pop(name)
        self.descriptions.pop(descr)

    def get_process_names(self):
        """
        Function to get all known process names
        """
        return list(self.names.keys())

    def get_process_descriptions(self):
        """
        Function to get all known process descriptions
        """
        return list(self.descriptions.keys())

    def __getitem__(self, key):
        """
        Operator overloading to simplify usage of the class
        """
        if type(key) is list:
            return self.descriptions[key[0]]
        else:
            return self.names[key]

    def __setitem__(self, key, value):
        """
        Operator overloading to simplify usage of the class
        """
        # [[]] call then key is a list
        if type(key) is list:
            if key[0] in self.descriptions:
                # update name if it is a known description
                self.names[value] = self.names.pop(self.descriptions[key[0]])
                self.descriptions[key[0]] = value
            else:
                # add description and name to the dicts
                self.descriptions[key[0]] = value
                self.names[value] = key[0]
        else:
            if key in self.names:
                # update description if it is a known name
                self.descriptions[value] = self.descriptions.pop(self.names[key])
                self.names[key] = value
            else:
                # add description and name to the dicts
                self.names[key] = value
                self.descriptions[value] = key

    def __str__(self):
        """
        Defines a string representation for the class so that its printable
        """ 
        return str(self.names) + str(self.descriptions)