def combinations_list(lst):
    """
    Generate all possible combinations of the elements in the given list.
    
    :param lst: List of elements to combine.
    :return: List of lists, where each inner list is a combination of elements from the input list.
    """
    result = [[]]
    for element in lst:
        result += [current_combination + [element] for current_combination in result]
    return result
