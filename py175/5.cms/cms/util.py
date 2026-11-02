def valid_filename(filename):
    if not filename:
        return False

    EXTENSIONS = ["txt", "md"]
    extension = filename.split('.')
    return len(extension) == 2 and extension[1] in EXTENSIONS

