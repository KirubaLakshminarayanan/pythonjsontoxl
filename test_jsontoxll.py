import os
import pytest
from jsontoxl import is_json, flatten_json, convert_to_excel
from datetime import datetime, timezone

# Sample JSON file paths for testing
SAMPLE_JSON_FILES = [
    'C:/Users/LKiruba/Desktop/Json_to_csv/Sample_Scenarios/Individual_json_File.json',
    'C:/Users/LKiruba/Desktop/Json_to_csv/Sample_Scenarios/nestedlist.json',

]


# Fixture to provide the sample JSON file paths
@pytest.fixture
def sample_json_files():
    return [os.path.abspath(os.path.join(os.path.dirname(__file__), 'Sample_Scenarios', file)) for file in
            SAMPLE_JSON_FILES]


# Test cases for is_json function
def test_is_json_valid(sample_json_files):
    for file_path in sample_json_files:
        assert is_json(file_path) is True


def test_is_json_invalid():
    invalid_file_path = 'C:/Users/LKiruba/Desktop/Json_to_csv/Sample_Scenarios/nestedlist.json/invalidjson.json'
    assert is_json(invalid_file_path) is False


# Test cases for flatten_json function
def test_flatten_json_dict():
    data = {
        "firstname": "John",
        "lastname": "Doe",
        "age": 30,
        "city": "New York",
        "email": "john.doe@example.com"
    }
    expected_flattened = {
        "firstname": "John",
        "lastname": "Doe",
        "age": 30,
        "city": "New York",
        "email": "john.doe@example.com"
    }
    assert flatten_json(data) == expected_flattened


def test_flatten_json_list():
    data = {
        "batch": {
            "batch_id": "001",
            "timestamp": "2024-04-10T08:00:00Z",
            "data": [
                {
                    "id": 1,
                    "name": "John",
                    "age": 30,
                    "city": "New York"
                },
                {
                    "id": 2,
                    "name": "Alice",
                    "age": 25,
                    "city": "Los Angeles"
                }
            ]
        }
    }

    expected_flattened = {
        "batch_batch_id": "001",
        "batch_timestamp": "2024-04-10T08:00:00Z",
        "batch_data_0_id": 1,
        "batch_data_0_name": "John",
        "batch_data_0_age": 30,
        "batch_data_0_city": "New York",
        "batch_data_1_id": 2,
        "batch_data_1_name": "Alice",
        "batch_data_1_age": 25,
        "batch_data_1_city": "Los Angeles"
    }

    assert flatten_json(data) == expected_flattened


def test_flatten_json_empty():
    assert flatten_json({}) == {}


# Test case for convert_to_excel function
def test_convert_to_excel(sample_json_files):
    success_count, failed_files_count = convert_to_excel(sample_json_files)
    # assert success_count == 1  # Assuming only one file succeeds conversion
    # assert failed_files_count == len(sample_json_files) - 1  # Assuming all other files fail conversion
    assert success_count == 2
    assert failed_files_count == len(sample_json_files) - 2


# Main entry point for running the tests
if __name__ == "__main__":
    pytest.main()
