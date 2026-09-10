def sequence(n):
    # Base cases for the Newman-Conway Sequence
    if n == 1 or n == 2:
        return 1
    
    # Recursive call to compute the nth number in the sequence
    return sequence(sequence(n - 1)) + sequence(n - sequence(n - 1))
