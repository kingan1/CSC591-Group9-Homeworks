import re
import sys



"""
    attempts to convert v to an int, float, bool, or keep as string
    
    :param v: String to convert
    :return: v converted to its type
"""
def coerce(v):
    types = [int, float]
    for t in types:
        try:
            return t(v)
        except:
            pass
    bool_vals = ["true", "false"]
    if v.lower() in bool_vals:
        return v.lower() == "true"
    return v


"""

    Class to manage commandline options. Underlying type is a dictionary

"""
class Options():
    
    """
        Init method, creates the options dictionary
    """
    def __init__(self):
        self.t = {}

    """
        Overrides the string representation. Prints the options and returns it

        :return: Dictionary of options
    """
    def __repr__(self):
        print(self.t)
        return str(self.t)
    
    """
        parse help string to extract a table of options
        sets the inner dictionary values
        
        :param help_string: String of settings
    """
    def parseCliSettings(self, help_string):
        # parse help string to extract a table of options
        # sets the inner dictionary values
        s = re.findall("\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", help_string)
        for k, v in s:
            self.t[k] = coerce(v)

        for k, v in self.items():  # for each possible option / CLI
            v = str(v)  # get the default value
            for n, x in enumerate(sys.argv):  # for each CLI passed in by the user
                if x == "-" + k[0] or x == "--" + k:  # if it matches one of the CLI
                    v = ( sys.argv[n+1] if n+1 < len(sys.argv) else False) or v == "False" and "true" or v == "True" and "false"
                    # set the value
                self.t[k] = coerce(v)

    """
        Gets all options
        
        :return: Dictionary of options
    """
    def items(self):
        return self.t.items()

    """
        Getter method
        
        :param key: Key of value to get
        :return: Value of options[key]
    """
    def __getitem__(self, key):
        return self.t[key]

    """
        Setter method
        
        :param key: Key of value to set
        :param value: Value to set
    """
    def __setitem__(self, key, value):
        self.t[key] = value


