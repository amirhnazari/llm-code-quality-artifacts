def next_power_of_2(n):
    """Find the smallest power of 2 greater than or equal to n."""
    if n <= 1:
        return 1
    p = 1
    while p < n:
        p <<= 1
    return p
