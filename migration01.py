import ciscoconfparse as ccp
import re

def extract_vrf_definitions(config_file=None):
    if config_file is None:
        raise ValueError


    config_parse = ccp.CiscoConfParse(config_file)

    return_list = list()
    for vrf_obj in config_parse.find_objects("^ip vrf"):
        vrf_name = vrf_obj.re_match_typed("^ip vrf (.*)")
        return_list.append(vrf_name)

    return return_list


def parse_configuration(filename=None):
    pass

def parse_mac_table(filename=None):
    if filename is None:
        raise(FileNotFoundError("No file name"))
    try:
        with open( filename, "r") as mac_table_file:
            vlan_mac_table = dict()

            for line in mac_table_file:
                mac_details = extract_mac(line)

                if not mac_details["VLAN"] in vlan_mac_table:
                    vlan_mac_table[mac_details["VLAN"]] = dict()

                vlan_mac_table[mac_details["VLAN"]][mac_details["MAC"]] = mac_details["port"]

            return vlan_mac_table

    except FileNotFoundError:
        exit(1)

def extract_mac(mac_line = None):
    if mac_line is None:
        raise(ValueError)

    extract = re.match(r"\*?\s+(?P<VLAN>\d+|---)\s+(?P<MAC>[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\s+(\w+)\s+(\w+)\s+(\d+|-)\s+(?P<port>.+)", mac_line)

    retval = {
        "VLAN" : extract.group("VLAN"),
        "MAC" : extract.group("MAC"),
        "port" : extract.group("port")
    }

    return retval

def get_interface_names(config_file = None):
    if config_file is None:
        raise ValueError

    config_parse = ccp.CiscoConfParse(config_file)

    return_list = list()

    for interface_obj in config_parse.find_objects("^interface"):
        interface_name = interface_obj.re_match_typed("^interface (.*)")
        return_list.append(interface_name)

    return return_list

def get_vrf_interfaces(config_file = None):
    if config_file is None:
        raise ValueError

    config_parse = ccp.CiscoConfParse(config_file)

def main():
    vlan_mac_table = parse_mac_table("data/dora.mac")
    for VLAN in vlan_mac_table:
        print(VLAN)
        for mac in vlan_mac_table[VLAN]:
            print(f"\t{mac}")

    vrf_list = extract_vrf_definitions("data/dora.confg")
    print(vrf_list)

    interface_list = get_interface_names("data/dora.confg")
    print(interface_list)

if __name__ == "__main__":
    main()