def count_first_elements(test_tup):
    """
    Count the number of elements that occur before the tuple element in the given tuple.
    
    :param test_tup: A tuple containing various types of elements including another tuple.
    :return: The count of elements before the first encountered tuple element.
    """
    return next(i for i, ele in enumerate(test_tup) if isinstance(ele, tuple))
