def primes_up_to(n):
    if n < 2:
        return []
    primes = [2]
    for num in range(3, n + 1, 2):
        is_prime = all(num % prime != 0 for prime in primes if prime * prime <= num)
        if is_prime:
            primes.append(num)
    return primes
