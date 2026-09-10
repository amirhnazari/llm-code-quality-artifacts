def set_left_most_unset_bit(n):
    if n == 0:
        return 1
    
    count = 0
    while n != 0:
        if (n & 1) == 0:
            n |= (1 << count)
            break
        n >>= 1
        count += 1
    
    return n

assert set_left_most_unset_bit(10) == 14
