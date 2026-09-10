def dict_depth(d):
    if isinstance(d, dict) and d:
        return 1 + max(map(dict_depth, d.values())) if any(isinstance(v, dict) for v in d.values()) else 0
    return 0

assert dict_depth({'a':1, 'b': {'c': {'d': {}}}}) == 4
