import random


def bytes_to_string(text):
    if hasattr(text, 'encode'):
        return cut_bytes_delimeter(str(text.encode('utf-8')))
    else:
        return cut_bytes_delimeter(str(text))


def cut_bytes_delimeter(text):
    return text[:-1][2:]


def boundary():
    return '-----' + str(int(random.random()*1e10))
