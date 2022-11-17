if __name__ == '__main__':
    x = 487
    i = 1
    while i:
        x = x + 1
        for i in range(2, int(x ** 0.5) + 1):
            if x % i == 0:
                break
        else:
            print(x)
            i = 0
