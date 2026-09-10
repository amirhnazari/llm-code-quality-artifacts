def newman_prime(n):
    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True

    def nsw_number(k):
        a, b = 1, 1
        for _ in range(k - 1):
            a, b = b, (b ** 2 - 1) // 2
        return b

    count = 0
    num = 2
    while True:
        if is_prime(nsw_number(num)):
            count += 1
            if count == n:
                return nsw_number(num)
        num += 1
