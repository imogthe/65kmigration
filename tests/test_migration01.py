import pytest
from migration01 import parse_configuration, parse_mac_table, extract_mac

class Test_parse_mac_table():
    def test_no_filename(self):
        with pytest.raises(FileNotFoundError, match=r"No file name"):
            retval = parse_mac_table()

    def test_invalid_filename(self):
        with pytest.raises(FileNotFoundError):
            retval = parse_mac_table()

    def test_returns_dict(self):
        return_value = parse_mac_table("../data/dora.mac")
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