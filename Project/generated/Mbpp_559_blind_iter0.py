def max_sub_array_sum(a, size):
    # Initialize variables to store the maximum sum and the current sum
    max_so_far = a[0]
    curr_max = a[0]

    # Iterate through the list starting from the second element
    for i in range(1, size):
        # Update the current maximum by including the current element or starting new from the current element
        curr_max = max(a[i], curr_max + a[i])
        # Update the overall maximum sum if the current maximum is greater
        max_so_far = max(max_so_far, curr_max)

    return max_so_far

# Test the function with the provided test case
assert max_sub_array_sum([-2, -3, 4, -1, -2, 1, 5, -3], 8) == 7
