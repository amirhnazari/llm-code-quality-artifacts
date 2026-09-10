def next_smallest_palindrome(n):
    # Increment the number by 1 to find the next potential palindrome
    n += 1
    # Loop until a palindrome is found
    while True:
        # Check if the number is equal to its reverse
        if str(n) == str(n)[::-1]:
            return n
        n += 1

# Test the function with the provided test case
assert next_smallest_palindrome(99) == 101
