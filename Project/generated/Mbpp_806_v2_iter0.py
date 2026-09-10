def max_run_uppercase(str1):
    # Initialize variables to keep track of the maximum run and current run lengths
    max_run = 0
    current_run = 0
    
    # Iterate through each character in the string
    for char in str1:
        # Check if the character is uppercase
        if char.isupper():
            # Increment the current run length
            current_run += 1
            # Update the maximum run length if the current run is longer
            max_run = max(max_run, current_run)
        else:
            # Reset the current run length if the character is not uppercase
            current_run = 0
    
    # Return the maximum run length found
    return max_run

# Test the function with the provided test case
assert max_run_uppercase('GeMKSForGERksISBESt') == 5
