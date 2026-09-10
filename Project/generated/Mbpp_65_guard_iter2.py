def recursive_list_sum(lst):
    """Flatten a list and sum all of its elements."""
    total = 0
    for i in lst:
        if isinstance(i, list):
            total += recursive_list_sum(i)
        else:
            total += i
    return total

# Test the function with the provided test case
assert recursive_list_sum(([1, 2, [3,4],[5,6]]))==21
