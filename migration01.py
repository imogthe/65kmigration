import ciscoconfparse as ccp
import re


def parse_configuration(filename=None):
    pass

def parse_mac_table(filename=None):
    if filename is None:
        raise(FileNotFoundError("No file name"))
    try:
        with open("data/" + filename, "r") as mac_table_file:
            return dict()

    except FileNotFoundError:
        exit(1)

def extract_mac(mac_line = None):
    if mac_line is None:
        raise(ValueError)

    extract = re.match(r"\*?\s+(?P<VLAN>\d+)\s+(?P<MAC>[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\s+(\w+)\s+(\w+)\s+(\d+)\s+(?P<port>.+)", mac_line)

    retval = {
        "VLAN" : extract.group("VLAN"),
        "MAC" : extract.group("MAC"),
        "port" : extract.group("port")
    }

    return retval

if __name__ == "__main__":
    main()