def odd_Equivalent(s, n):
    # Count the number of '1's in the binary string
    count = s.count('1')
    
    # If there are no '1's or all '1's, return 0 as no rotation will result in an odd value
    if count == 0 or count == len(s):
        return 0
    
    # Otherwise, return the number of rotations that will result in an odd value
    return (len(s) - count + 1)
