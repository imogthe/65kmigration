import pytest
from migration01 import parse_configuration, parse_mac_table, extract_mac, extract_vrf_definitions
from migration01 import get_interface_names, get_vrf_interfaces

class Test_parse_mac_table():
    def test_no_filename(self):
        with pytest.raises(FileNotFoundError, match=r"No file name"):
            retval = parse_mac_table()

    def test_invalid_filename(self):
        with pytest.raises(FileNotFoundError):
            retval = parse_mac_table()

    def test_returns_dict(self):
        return_value = parse_mac_table("data/dora.mac")
        assert type(return_value) is dict

class Test_extract_mac():
    def test_extract_returns_dict(self):
        test_string = "  3337  0050.56b8.0e42   dynamic  Yes        600   Po64"

        return_value = extract_mac(test_string)

        assert type(return_value) is dict

    def test_extract_no_argument(self):
        with pytest.raises(ValueError):
            retval = extract_mac()

    def test_extract_with_asterisk(self):
        test_string = "*  274  984b.e172.5c5b   dynamic  Yes        600   Po20"

        retval = extract_mac(test_string)
        assert type(retval) is dict
        assert type(retval["VLAN"]) is str
        assert retval["VLAN"] == "274"
        assert retval["MAC"] == "984b.e172.5c5b"
        assert retval["port"] == "Po20"

    def test_extract_without_asterisk(self):
        test_string = "  3337  0050.56b8.0e42   dynamic  Yes        600   Po64"
        retval = extract_mac(test_string)
        assert type(retval) is dict
        assert type(retval["VLAN"]) is str
        assert retval["VLAN"] == "3337"
        assert retval["MAC"] == "0050.56b8.0e42"
        assert retval["port"] == "Po64"

    def test_extract_no_port(self):
        test_string = "* 3600  0100.5e48.7940    static  Yes          -   "
        retval = extract_mac(test_string)
        assert type(retval) is dict
        assert type(retval["VLAN"]) is str
        assert retval["VLAN"] == "3600"
        assert retval["MAC"] == "0100.5e48.7940"
        assert retval["port"] == " "

    def test_extract_router_mac(self):
        test_string = "*  ---  0000.0000.0000    static  No           -   Router"
        retval = extract_mac(test_string)
        assert type(retval) is dict
        assert type(retval["VLAN"]) is str
        assert retval["VLAN"] == "---"
        assert retval["MAC"] == "0000.0000.0000"
        assert retval["port"] == "Router"

class Test_get_vrf_definitions():

    def setup_method(self):
        self.vrf_test_data_file = "tests/test_data/vrfs.txt"
    def test_no_file(self):
        with pytest.raises(ValueError):
            retval = extract_vrf_definitions()

    def test_invalid_file(self):
        with pytest.raises(RuntimeError):
            retval = extract_vrf_definitions("tjobing.txt")

    def test_returns_list(self):
        retval = extract_vrf_definitions(self.vrf_test_data_file)

        assert type(retval) is list

    def test_extract_vrf_list(self):
        retval = extract_vrf_definitions(self.vrf_test_data_file)
        desired_result = ["gprs-gb","gprs-gi","gprs-gn"]

        assert all(
            a == b for a,b in zip(retval, desired_result)
        )

class Test_get_interfaces():
    def setup_method(self):
        self.interface_config_file = "tests/test_data/interfaces.txt"

    def test_no_config_file(self):
        with pytest.raises(ValueError):
            retval = get_interface_names()

    def test_get_all_interfaces(self):
        desired_result = [
            "Port-channel1",
            "Port-channel5",
            "Loopback200",
            "TenGigabitEthernet1/1/5",
            "TenGigabitEthernet1/1/6",
            "GigabitEthernet1/3/1",
            "GigabitEthernet1/3/2",
            "GigabitEthernet1/3/3",
            "GigabitEthernet1/3/4"

        ]

        retval = get_interface_names(self.interface_config_file)

        assert all(
            a == b for a, b in zip(retval, desired_result)
        )

class Test_get_vrf_interfaces():
    def setup_method(self):
        self.config_file = "tests/test_data/vrf_interfaces.txt"

    def test_no_file(self):
        with pytest.raises(ValueError):
            retval = get_vrf_interfaces()

    def test_invalid_file(self):
        with pytest.raises(RuntimeError):
            retval = get_vrf_interfaces("jallaballa.txt")

