######################################################.
#          This file stores functions used           #
#                in multiple modules                 #
######################################################.

import os
import sys
import time
import getopt
import glob
import yaml
import ast
from pathlib import Path
from robert.argument_parser import set_options, var_dict


robert_version = "0.0.1"
time_run = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
robert_ref = f"ROBERT v {robert_version}, Alegre-Requena, J. V.; Dalmau, D., 2023. https://github.com/jvalegre/robert"


# load paramters from yaml file
def load_from_yaml(self):
    """
    Loads the parameters for the calculation from a yaml if specified. Otherwise
    does nothing.
    """

    txt_yaml = f"\no  Importing ROBERT parameters from {self.varfile}"
    error_yaml = False
    # Variables will be updated from YAML file
    try:
        if os.path.exists(self.varfile):
            if os.path.splitext(self.varfile)[1] in [".yaml", ".yml", ".txt"]:
                with open(self.varfile, "r") as file:
                    try:
                        param_list = yaml.load(file, Loader=yaml.SafeLoader)
                    except yaml.scanner.ScannerError:
                        txt_yaml = f'\nx  Error while reading {self.varfile}. Edit the yaml file and try again (i.e. use ":" instead of "=" to specify variables)'
                        error_yaml = True
        if not error_yaml:
            for param in param_list:
                if hasattr(self, param):
                    if getattr(self, param) != param_list[param]:
                        setattr(self, param, param_list[param])

    except UnboundLocalError:
        txt_yaml = "\nx  The specified yaml file containing parameters was not found! Make sure that the valid params file is in the folder where you are running the code."

    return self, txt_yaml


# class for logging
class Logger:
    """
    Class that wraps a file object to abstract the logging.
    """

    # Class Logger to writargs.input.split('.')[0] output to a file
    def __init__(self, filein, append, suffix="dat"):
        self.log = open(f"{filein}_{append}.{suffix}", "w")

    def write(self, message):
        """
        Appends a newline character to the message and writes it into the file.

        Parameters
        ----------
        message : str
           Text to be written in the log file.
        """
        self.log.write(f"{message}\n")
        print(f"{message}\n")

    def fatal(self, message):
        """
        Writes the message to the file. Closes the file and raises an error exit

        Parameters
        ----------
        message : str
           text to be written in the log file.
        """
        self.write(message)
        self.finalize()
        raise SystemExit(1)

    def finalize(self):
        """
        Closes the file
        """
        self.log.close()


def move_file(destination, source, file):
    """
    Moves files from the source folder to the destination folder and creates
    the destination folders when needed.

    Parameters
    ----------
    destination : str
        Path to the destination folder
    src : str
        Path to the source folder
    file : str
        Full name of the file (file + extension)
    """

    destination.mkdir(exist_ok=True, parents=True)
    filepath = source / file
    try:
        filepath.rename(destination / file)
    except FileExistsError:
        filepath.replace(destination / file)


def command_line_args():
    """
    Load default and user-defined arguments specified through command lines. Arrguments are loaded as a dictionary
    """

    # First, create dictionary with user-defined arguments
    kwargs = {}
    available_args = ["help"]
    bool_args = [
        "curate",
        "generate",
        "outliers",
        "predict",
    ]

    for arg in var_dict:
        if arg in bool_args:
            available_args.append(f"{arg}")
        else:
            available_args.append(f"{arg} =")

    try:
        opts, _ = getopt.getopt(sys.argv[1:], "h", available_args)
    except getopt.GetoptError as err:
        print(err)
        sys.exit()

    for arg, value in opts:
        if arg.find("--") > -1:
            arg_name = arg.split("--")[1].strip()
        elif arg.find("-") > -1:
            arg_name = arg.split("-")[1].strip()
        if arg_name in bool_args:
            value = True
        if value == "None":
            value = None
        if arg_name in ("h", "help"):
            print(f"o  ROBERT v {robert_version} is installed correctly! For more information about the available options, see the documentation in https://github.com/jvalegre/robert")
            sys.exit()
        else:
            # this "if" allows to use * to select multiple files in multiple OS
            if arg_name.lower() == 'files' and value.find('*') > -1:
                kwargs[arg_name] = glob.glob(value)
            else:
                # this converts the string parameters to lists
                if arg_name.lower() in ["discard"]:
                    if not isinstance(value, list):
                        try:
                            value = ast.literal_eval(value)
                        except (SyntaxError, ValueError):
                            # this line fixes issues when using "[X]" or ["X"] instead of "['X']" when using lists
                            if arg_name.lower() in ["discard"]:
                                value = value.replace('[',']').replace(',',']').split(']')
                                while('' in value):
                                    value.remove('')
                kwargs[arg_name] = value

    # Second, load all the default variables as an "add_option" object
    args = load_variables(kwargs, "command")

    return args


def load_variables(kwargs, robert_module, create_dat=True):
    """
    Load default and user-defined variables
    """

    # first, load default values and options manually added to the function
    self = set_options(kwargs)

    # this part loads variables from yaml files (if varfile is used)
    txt_yaml = ""
    if self.varfile is not None:
        self, txt_yaml = load_from_yaml(self)
            
    # start a log file
    if create_dat:
        logger_1 = 'ROBERT'
        logger_1, logger_2 = robert_module.upper(), "data"

        if txt_yaml not in [
            "",
            f"\no  Importing ROBERT parameters from {self.varfile}",
            "\nx  The specified yaml file containing parameters was not found! Make sure that the valid params file is in the folder where you are running the code.\n",
        ]:
            self.log = Logger(self.initial_dir / logger_1, logger_2)
            self.log.write(txt_yaml)
            self.log.finalize()
            os.chdir(self.initial_dir)
            sys.exit()

        if not self.command_line:
            self.log = Logger(self.initial_dir / logger_1, logger_2)
        else:
            # prevents errors when using command lines and running to remote directories
            path_command = Path(f"{os.getcwd()}")
            self.log = Logger(path_command / logger_1, logger_2)

        self.log.write(f"ROBERT v {robert_version} {time_run} \nCitation: {robert_ref}\n")

        if self.command_line:
            self.log.write(f"Command line used in ROBERT: robert {' '.join([str(elem) for elem in sys.argv[1:]])}\n")

    return self


def read_file(initial_dir, w_dir, file):
    """
    Reads through a file and retrieves a list with all the lines.
    """

    os.chdir(w_dir)
    outfile = open(file, "r")
    outlines = outfile.readlines()
    outfile.close()
    os.chdir(initial_dir)

    return outlines
