def str_to_bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")


def str_to_none(v):
    if v is '':
        return None
    else:
        return v
