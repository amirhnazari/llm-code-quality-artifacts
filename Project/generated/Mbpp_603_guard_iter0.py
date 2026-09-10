def get_ludic(n):
    # Initialize the list of ludic numbers with the first two numbers
    ludics = [1, 2]
    
    # Iterate from 3 to n to find all ludic numbers up to n
    for i in range(3, n + 1):
        # Check if the number is a ludic number by ensuring it's not divisible by any previous ludic number
        if all(i % l != 0 for l in ludics):
            ludics.append(i)
    
    # Return the list of ludic numbers up to n
    return ludics

# Test the function with the provided test case
assert get_ludic(10) == [1, 2, 3, 5, 7]
