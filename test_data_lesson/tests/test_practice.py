import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.json_utils import read_json
from src.csv_utils import read_csv
from src.xml_utils import get_element_from_xml


def test_json_loading():
    data = read_json("users.json")
    assert len(data) == 2
    assert data[0]["name"] == "Alice"

def test_csv_loading():
    data = read_csv("users.csv")
    assert len(data) == 2
    assert data[1]["name"] == "David"

def get_xml_element():
    port = get_element_from_xml("config.xml", element="database/port")
    assert port == "5432"

if __name__ == "__main__":
    test_json_loading()
    test_csv_loading()
    get_xml_element()
    print("All tests passed!")