def primes_up_to(n):
    if n < 2:
        return []
    primes = [2]
    for num in range(3, n + 1, 2):
        if all(num % prime != 0 for prime in primes if prime * prime <= num):
            primes.append(num)
    return primes
