def is_Sub_Array(main_list, sub_list):
    """
    Check if sub_list is a sublist of main_list.

    :param main_list: List to be checked against.
    :param sub_list: Sublist to check for.
    :return: True if sub_list is a sublist of main_list, False otherwise.
    """
    return all(item in main_list for item in sub_list)
