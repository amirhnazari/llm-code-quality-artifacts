def is_woodall(n):
    # Check if n is less than 1, as Woodall numbers are greater than 0
    if n < 1:
        return False
    
    # Initialize the variable to store the current number being checked
    x = 1
    
    # Loop until x is greater than or equal to n
    while x < n:
        # Check if x is a Woodall number by comparing it with n
        if x == n:
            return True
        
        # Update x to the next Woodall number
        x *= 2
        x -= 1
    
    # If no Woodall number matches n, return False
    return False

# Test the function with the provided test case
assert is_woodall(383) == True
