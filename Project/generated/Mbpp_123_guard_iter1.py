def amicable_numbers_sum(n):
    """
    Write a function to sum all amicable numbers from 1 to a specified number.
    
    :param n: Upper limit for finding amicable numbers
    :return: Sum of all amicable numbers up to n
    """
    # Helper function to calculate the sum of proper divisors of a number
    def sum_of_divisors(x):
        return sum(i for i in range(1, x) if x % i == 0)
    
    # Initialize total sum of amicable numbers
    total = 0
    
    # Iterate through all numbers from 2 to n
    for num in range(2, n + 1):
        div_sum = sum_of_divisors(num)
        
        # Check if the sum of divisors is greater than the number and forms an amicable pair
        if div_sum > num and sum_of_divisors(div_sum) == num:
            total += num
    
    return total

# Test the function with the provided test case
assert amicable_numbers_sum(999) == 504
