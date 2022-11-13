def pretty_print(n, char):
    for i in range(n):
        for j in range(n):
            if i == 0 or i == n - 1 or j == 0 or j == n - 1:
                print(char, end=' ')
            else:
                print(' ', end=' ')
        print()


if __name__ == '__main__':
    n = 7
    char = '!'
    pretty_print(n, char)
