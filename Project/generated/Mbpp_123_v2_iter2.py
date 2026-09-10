def amicable_numbers_sum(n):
    def sum_of_divisors(x):
        return sum(i for i in range(1, x) if x % i == 0)
    
    total = 0
    
    for num in range(2, n + 1):
        div_sum = sum_of_divisors(num)
        if num < div_sum and sum_of_divisors(div_sum) == num:
            total += num
    
    return total

assert amicable_numbers_sum(999) == 504
