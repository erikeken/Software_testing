def toEnglish(n):
    """Convert a number to English."""
    numbers = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
        "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
        "eighteen", "nineteen", "twenty", "twenty one"
    ]
    tens = ["","","twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    numberOfTens = n // 10
    numberOfUnits = n % 10
    if n in range(0, 21):
        return (numbers[n])
    return_string=tens[numberOfTens]
    if numberOfUnits > 0:
        return_string=return_string+" "+numbers[numberOfUnits]
    return return_string
# print(toEnglish(21))
