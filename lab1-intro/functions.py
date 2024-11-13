# functions.py

import math
import pytest
PI = math.pi

def count_words(s):
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    words = s.split()
    non_empty_words = [word for word in words if word]
    return len(non_empty_words)

def count_total_characters(word_list, num_digits=2):
    total_chars = len(''.join(word_list))
    return f"{total_chars:0{num_digits}d}"

def calculate_circle_area(radius):
    area = PI * (radius ** 2)
    return round(area, 4)

#print(count_words())