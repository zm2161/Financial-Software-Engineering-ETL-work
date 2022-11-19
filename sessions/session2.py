def swap(a, b):
    """
    Exchange values without creating another variable.
    Params
    ---
    a:int/float
    b:int/float

    Return
    ---
    two ints/floats
    """
    b, a = a, b
    return a, b


def palindrome(st):
    """
    Given a word string, check if it is a palindrome
    Params
    ---
    st:string
    Return
    ---
    Bool
    """

    return st == st[::-1]


def fizzbuzz():
    """
    Print integers from 1 to 100 (inclusive), using following rules:
    for multiples of 3, print “Fizz” (instead of the number);
    for multiples of 5, print “Buzz” (instead of the number);
    for multiples of both 3 and 5, print “FizzBuzz” (instead of the number)

    Return
    ---
    print
    """
    for i in range(1, 101):
        if i % 3 == 0 and i % 5 == 0:
            print('FizzBuzz')
        elif i % 5 == 0:
            print('Buzz')
        elif i % 3 == 0:
            print('Fizz')
        else:
            print(i)


def next_prime(x):
    """
    Given an arbitrary integer x, returns the next
    biggest prime number
    Params x:int
    Return int

    """

    def is_prime(y):
        """
        Given an arbitrary integer y, check if it is a prime
        """
        return all(y % i for i in range(2, y))

    return min([a for a in range(x + 1, 2 * x) if is_prime(a)])


# Extra credit
def pretty_print(n, char):
    """
    Params
    ------
    n: int
         number of lines
    char: str
        char

    Return
    ------
        print the string based on format"""

    if not isinstance(n, int):
        print('first parameter should be a integer')
    if n < 0:
        print('error in n')
    if not isinstance(char, str):
        print('second parameter should be a string')
    for i in range(n):
        str_res = ''
        char_list = []
        if i == 0 or i == n - 1:
            print(char * n)
        else:
            # add first char
            char_list.append(char)
            for j in range(n - 2):
                char_list.append(' ')
            char_list.append(char)

            print(str_res.join(char_list))


# second extra credit
def max_pair_sum(arr):
    """
    Function that return sum of maximum two elements from array
    Params arr: array
    Return int
    """
    n = len(arr)

    if (arr[0] > arr[1]):
        fir_max = arr[0]
        sec_max = arr[1]
    else:
        fir_max = arr[1]
        sec_max = arr[0]
    for i in range(2, n):
        if arr[i] > fir_max:
            sec_max = fir_max
            fir_max = arr[i]
        elif arr[i] > sec_max:
            sec_max = arr[i]
    return fir_max + sec_max


def count_pairs_with(n, squares, nums):
    """
    Function that returns the count of numbers that can be added with n to give a square
    Params
    ---
    n:int
    squares: array
    nums:array
    Return
    ---
    count:int
    """

    count = 0
    for i in range(len(squares)):
        temp = squares[i] - n
        if temp > n and temp in nums:
            count += 1
    return count


def get_squares(n):
    """
    GetSquares returns a list of all perfect squares upto n
    Params
    ---
    n:int
    Return
    ---
    squares: array
    """
    squares = []
    curr = 1
    i = 1
    while (curr <= n):
        squares.append(curr)
        i += 1
        curr = int(pow(i, 2))
    return squares


def count_square(arr):
    """
    Count pair sum that creates a perfect square in arr
    """
    n = len(arr)
    max_sum = max_pair_sum(arr)
    squares = get_squares(max_sum)
    count = 0
    nums = []
    for i in range(n):
        nums.append(arr[i])
    for i in range(n):
        count += count_pairs_with(arr[i], squares, nums)
    return count


if __name__ == '__main__':
    print('swap 1 and 2 is ',swap(1, 2))
    print('level is palindrome ',palindrome('level'))
    fizzbuzz()
    print('next prime of 12 is ', next_prime(12))
    pretty_print(4, '0')
    arr = [0, 2, 3, 4, 6]
    print('Count of perfect squares:', count_square(arr))
