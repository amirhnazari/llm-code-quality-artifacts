def find_length(s):
    max_diff = curr_diff = 0
    for char in s:
        curr_diff += (2 * (char == '1') - 1)
        if curr_diff < 0:
            curr_diff = 0
        max_diff = max(max_diff, curr_diff)
    return max_diff
