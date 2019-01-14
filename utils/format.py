# Blue, Green, Red
def color_to_string(color):
    string = ""

    for digit in color:
        string += str(digit) + '|'

    return string[:-1]

def string_to_color(string):
    return string.split('|')
