def is_Sub_Array(l1, l2):
    """
    Check if list l2 is a sublist of list l1.
    
    :param l1: List to be checked against.
    :param l2: Sublist to check for.
    :return: True if l2 is a sublist of l1, False otherwise.
    """
    return all(item in l1 for item in l2)
