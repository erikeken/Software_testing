import math
import pytest

def task1():
    a = input("Your input here: ")

    print(a.capitalize())

def task2(a,b):
    if (a.is_integer() and b.is_integer()):
        print(int(a+b))
    else:
        print("needs to be integer")

def count_words(s):
    words = s.split()  # Split by spaces
    non_empty_words = [word for word in words if word]  # Exclude empty strings
    return len(non_empty_words)

def count_total_characters(word_list, num_digits=2):
    total_chars = len(''.join(word_list))  # Concatenate and count characters
    return f"{total_chars:0{num_digits}d}"  # Format to specified digits with leading zeros if needed


PI = math.pi  # Set the global Pi constant

def calculate_circle_area(radius):
    area = PI * (radius ** 2)
    return round(area, 4)  # Round to 4 decimal places


