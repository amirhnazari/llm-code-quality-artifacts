def recursive_list_sum(lst):
    # Initialize the total sum using a generator expression
    return sum(recursive_list_sum(i) if isinstance(i, list) else i for i in lst)
