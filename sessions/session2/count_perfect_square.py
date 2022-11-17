import math


def count_perfect_square(array1):
    length = len(array1)
    count = 0

    for i in range(length):
        for j in range(i + 1, length):
            if int(math.sqrt(array1[i] + array1[j])) ** 2 == array1[i] + array1[j]:
                count = count + 1

    return count


if __name__ == '__main__':
    numbers = [4, 7, 3, 7, 9, 3, 2, 7, 6, 9, 4, 3, 7, ]
    print(count_perfect_square(numbers))
