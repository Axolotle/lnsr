from time import strftime
from math import ceil

from .data import rulers_per_box, box_per_container


def number_to_string(number):
    text = str(number)
    splittedText = [text[(i-3 if i-3 > 0 else 0):i]
                    for i in range(len(text), -1, -3)]
    return ' '.join(reversed(splittedText))

def get_content_numbers(specimen_number):
    cardboard = ceil(specimen_number / rulers_per_box)
    return {
        'cardboard': number_to_string(cardboard),
        'container': number_to_string(ceil(cardboard / box_per_container)),
        'date': get_date_string()
    }

def get_date_string():
    return strftime('%d/%m/%y à %Hh%M')
