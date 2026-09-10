def find_length(s):
    # Initialize variables to store the maximum difference and current difference
    max_diff = 0
    curr_diff = 0
    
    # Iterate through each character in the string
    for char in s:
        # Increment current difference if '1' is encountered, decrement otherwise
        curr_diff += (1 if char == '1' else -1)
        
        # If current difference becomes negative, reset it to zero
        if curr_diff < 0:
            curr_diff = 0
        
        # Update maximum difference if current difference is greater
        max_diff = max(max_diff, curr_diff)
    
    return max_diff
