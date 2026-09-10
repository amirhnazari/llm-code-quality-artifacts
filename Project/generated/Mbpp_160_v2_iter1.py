def find_solution(a, b, n):
    for x in range(n // a + 1):
        y = (n - a * x) / b
        if y.is_integer() and y >= 0:
            return (x, int(y))
    return None
