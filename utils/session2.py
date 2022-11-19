def swap(a,b):
    '''
    Exchange values without creating another variable.
    Params
    ---
    a:int/float
    b:int/float

    Return
    ---
    two ints/floats
    '''
    b,a=a,b
    print(a,b)
swap(1,2)
def palindrome(st):
    '''
    Given a word string, check if it is a palindrome 
    '''
    return st==st[::-1]
palindrome('level')
def fizzbuzz():
    '''
    Print integers from 1 to 100 (inclusive), using following rules: 
    for multiples of 3, print “Fizz” (instead of the number); 
    for multiples of 5, print “Buzz” (instead of the number); 
    for multiples of both 3 and 5, print “FizzBuzz” (instead of the number)
    '''
    for i in range(1,101):
        if i % 3 == 0 and i % 5 == 0:print('FizzBuzz')
        elif i % 5 == 0:print('Buzz')
        elif i % 3 == 0:print('Fizz')
        else:print(i)

def is_prime(x):
    '''
    Given an arbitrary integer x, check if it is a prime
    '''
    return all(x%i for i in range(2,x))
def next_prime(x):
    '''
    Given an arbitrary integer x, returns the next 
    biggest prime number
    '''
    return min([a for a in range(x+1,2*x) if is_prime(a)])
print(next_prime(12))
#Extra credit
def pretty_print(n, char):
    '''  
    Params
    ------
    n: int
         number of lines 
    char: str
        char
    
    Return
    ------
        print the string based on format'''
        
    if not isinstance(n, int):
        print('first parameter should be a integer')
    if n<0:
        print('error in n')
    if not isinstance(char, str):
        print('second parameter should be a string')
    for i in range(n):
        str_res=''
        char_list=[]
        if i == 0 or i ==n-1:
            print(char*n)
        else:
            #add first char
            char_list.append(char)
            for j in range(n-2):
                char_list.append(' ')
            char_list.append(char)

            print(str_res.join(char_list))
pretty_print(4,'0')
def MaxPairSum(arr):
    """
    Function that return sum of maximum two elements from array
    """
    n=len(arr)
    firMax,secMax=0,0
    if (arr[0]>arr[1]):
        firMax=arr[0]
        secMax=arr[1]
    else:
        firMax=arr[1]
        secMax=arr[0]
    for i in range(2,n):
        if (arr[i]>firMax):
            secMax=firMax
            firMax=arr[i]
        elif (arr[i]>secMax):
            secMax=arr[i]
    return firMax+secMax
    
def CountPairsWith(n,squares,nums):
    """
    Function that returns the count of numbers that can be added with n to give a square
    """  
    count=0
    for i in range(len(squares)):
        temp=squares[i]-n
        if (temp>n and temp in nums):
            count+=1
    return count

def GetSquares(n):
    """
    GetSquares returns a list of all perfect squares upto n
    """
    squares=[]
    curr=1
    i=1
    while (curr<=n):
        squares.append(curr)
        i+=1
        curr=int(pow(i,2))
    return squares

def CountSquare(arr):
    """
    Count pair sum that creates a perfect square in arr
    """
    n=len(arr)
    maxsum=MaxPairSum(arr)
    squares=GetSquares(maxsum)
    count=0
    nums=[]
    for i in range(n):
        nums.append(arr[i])
    for i in range(n):
        count+=CountPairsWith(arr[i],squares,nums)
    return count

arr=[0,2,3,4,6]
print(CountSquare(arr))