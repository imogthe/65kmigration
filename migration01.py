import ciscoconfparse as ccp
import re


def parse_configuration(filename=None):
    pass

def parse_mac_table(filename=None):
    if filename is None:
        raise(FileNotFoundError("No file name"))
    with open("data/" + filename, "r") as mac_table_file:
        pass


if __name__ == "__main__":
    main()