import pytest
from migration01 import parse_configuration, parse_mac_table

class test_parse_mac_table():
    def test_no_filename(self):
        with raises(FileNotFoundError, match=r"No file name"):
            retval = parse_mac_table()
    # def test_returns_dict(self):
    #     return_value = parse_mac_table()