def bytes_to_string(text):
    return cut_bytes_delimeter(str(text.encode('utf-8')))


def cut_bytes_delimeter(text):
    return text[:-1][2:]
