def primes_up_to(n):
    if n < 2:
        return []
    primes = [2]
    for num in range(3, n + 1, 2):
        is_prime = True
        for prime in primes:
            if prime * prime > num:
                break
            if num % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes
