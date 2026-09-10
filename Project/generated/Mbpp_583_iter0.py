def catalan_number(n):
    # Base case: the first Catalan number is 1
    if n == 0:
        return 1
    
    # Initialize a list to store the Catalan numbers up to n
    catalan = [0] * (n + 1)
    catalan[0], catalan[1] = 1, 1
    
    # Calculate each Catalan number using the recursive formula
    for i in range(2, n + 1):
        catalan[i] = sum(catalan[j] * catalan[i - j - 1] for j in range(i))
    
    # Return the nth Catalan number
    return catalan[n]
