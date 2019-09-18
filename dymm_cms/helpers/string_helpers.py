def str_to_bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")


def str_to_none(v):
    if v is '':
        return None
    else:
        return v


def to_camel_case(snake_string, split_item):
    snakes = snake_string.split(split_item)
    camel_string = snakes[0] + "".join(map(str.capitalize, snakes[1:]))
    return camel_string
