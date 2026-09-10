def newman_prime(n):
    """
    Find the nth Newman-Shanks-Williams (NSW) prime number.
    
    Args:
    n (int): The position of the NSW prime to find.
    
    Returns:
    int: The nth NSW prime number.
    """
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True

    a, b = 0, 1
    count = 0
    while True:
        nsw_number = 2 * b + a
        a, b = b, nsw_number
        if is_prime(nsw_number):
            count += 1
            if count == n:
                return nsw_number
