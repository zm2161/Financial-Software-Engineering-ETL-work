if __name__ == '__main__':
    b = 43
    a = 67
    print(a, b)
    a = a + b
    b = a - b
    a = a - b
    print(a, b)
    a, b = b, a
    print(a, b)
