def recursive_list_sum(lst):
    return sum(recursive_list_sum(i) if isinstance(i, list) else i for i in lst)
