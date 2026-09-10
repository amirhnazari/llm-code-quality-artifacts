def set_left_most_unset_bit(n):
    if n == 0:
        return 1
    
    count = 0
    while n != 0:
        if (n & 1) == 0:
            return n | (1 << count)
        n >>= 1
        count += 1
    
    return n | (1 << count)

assert set_left_most_unset_bit(10) == 14
