def normalize_field(name):
    if type(name) != int and not name and name is not None:
        return 'Blank'
    elif name is None:
        return 'Null'
    else:
        return name


def make_list(data):
    if not data:
        data = []
    elif not isinstance(data, list):
        data = [data]

    return data
