def find_solution(a, b, n):
    # Iterate through possible values of x
    for x in range(n // a + 1):
        # Calculate the corresponding value of y
        if (n - a * x) % b == 0:
            y = (n - a * x) // b
            return (x, y)
    # Return None if no solution is found
    return None
