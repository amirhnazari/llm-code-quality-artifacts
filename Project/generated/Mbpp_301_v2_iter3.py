def dict_depth(d):
    if not isinstance(d, dict) or not d:
        return 0
    return 1 + max((dict_depth(v) for v in d.values() if isinstance(v, dict)), default=0)
