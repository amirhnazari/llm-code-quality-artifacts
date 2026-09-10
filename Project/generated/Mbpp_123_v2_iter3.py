def amicable_numbers_sum(n):
    def sum_of_divisors(x):
        return sum(i for i in range(1, x) if x % i == 0)
    
    total = sum(num for num in range(2, n + 1) if num < sum_of_divisors(num) and sum_of_divisors(sum_of_divisors(num)) == num)
    
    return total

assert amicable_numbers_sum(999) == 504
