def max_sub_array_sum(a):
    max_so_far = curr_max = a[0]
    for num in a[1:]:
        curr_max = max(num, curr_max + num)
        max_so_far = max(max_so_far, curr_max)
    return max_so_far

assert max_sub_array_sum([-2, -3, 4, -1, -2, 1, 5, -3]) == 7
