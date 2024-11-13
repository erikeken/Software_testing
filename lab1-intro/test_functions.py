import pytest
from functions import count_words


# Parameterized test for valid inputs
@pytest.mark.parametrize("input_string, expected_count", [
    ("Hello world", 2),
    ("   This is a test   ", 4),
    ("One", 1),
    ("", 0),
    ("This   has   extra spaces", 4),
    ("Another test with five words", 5),
    ("  Leading and trailing spaces   ", 4)
])
def test_count_words_valid(input_string, expected_count):
    assert count_words(input_string) == expected_count
# Test for invalid input types
@pytest.mark.parametrize("invalid_input", [
    123,                 # Integer
    12.34,               # Float
    ["list", "of", "words"],  # List
    {"key": "value"},    # Dictionary
    None                 # NoneType
])
def test_count_words_invalid(invalid_input):
    with pytest.raises(TypeError):
        count_words(invalid_input)