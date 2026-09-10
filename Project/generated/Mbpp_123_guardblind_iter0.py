def amicable_numbers_sum(n):
    # Helper function to calculate the sum of proper divisors of a number
    def sum_of_divisors(x):
        return sum([i for i in range(1, x) if x % i == 0])
    
    # Initialize total sum of amicable numbers
    total = 0
    
    # Iterate through all numbers from 2 to n
    for num in range(2, n + 1):
        # Calculate the sum of divisors of the current number
        sum_divs = sum_of_divisors(num)
        
        # Check if the sum of divisors is greater than the number and forms an amicable pair
        if sum_divs > num and sum_of_divisors(sum_divs) == num:
            total += num
    
    return total

# Test the function with the provided test case
assert amicable_numbers_sum(999) == 504
