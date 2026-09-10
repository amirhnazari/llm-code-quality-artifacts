def is_undulating(n):
    # Convert the number to a string to easily access individual digits
    s = str(n)
    
    # Check if the length of the number is less than 3 or not even
    if len(s) < 3 or len(s) % 2 != 0:
        return False
    
    # Iterate through the string in steps of 2 to check for undulating pattern
    for i in range(2, len(s), 2):
        # If any two consecutive pairs of digits are not equal, return False
        if s[i] != s[i - 2]:
            return False
    
    # If all checks pass, the number is undulating
    return True

# Test the function with the provided test case
assert is_undulating(1212121) == True
