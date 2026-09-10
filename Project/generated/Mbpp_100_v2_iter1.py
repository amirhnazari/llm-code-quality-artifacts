def next_smallest_palindrome(n):
    n += 1
    while str(n) != str(n)[::-1]:
        n += 1
    return n

# Test the function with the provided test case
assert next_smallest_palindrome(99) == 101
