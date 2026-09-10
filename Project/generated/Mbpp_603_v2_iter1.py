def get_ludic(n):
    ludics = [1, 2]
    for i in range(3, n + 1):
        if all(i % l != 0 for l in ludics):
            ludics.append(i)
    return ludics

assert get_ludic(10) == [1, 2, 3, 5, 7]
