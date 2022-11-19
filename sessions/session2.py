#!/usr/bin/env python
# coding: utf-8


#exercise1
A=14
B=41
A,B=B,A
print("A=",A,"B=",B)

#exercise2
def check_if_palindrome(str):
    """Given a word string, check if it is a palindrome
    
    Parameters
    ------
    str:string
         The word to be checked
         
    Returns
    ------
    boolean
        return True if the word is a palindrome
    """
    reversed = str[::-1]
    return str == reversed

#exercise3
for integers in range(1,101):
    if integers % 15 == 0:
        print('FizzBuzz')
        continue
    elif integers % 3==0:
        print('Fizz')
        continue
    elif integers % 5 == 0:
        print('Buzz')
        continue
    print(integers)
    
#exercise4
def next_prime(x):
    """Given a integer x, find its next prime number
    
    Parameters
    ------
    x:integer
         
    Returns
    ------
    integer
        return x's next prime number
    """
    prime=x+1
    while True:
        if is_prime(prime)==False:
            prime+=1
        else:
            break
    return prime
        

def is_prime(x):
    for i in range(2,int(x/2)+1):
        if (x%i) == 0:
            return False
    return True

#exercise5
def pretty_print(n, char):
    if n ==1:
        print(char*n)
    if n == 2:
        print(char*n)
        print(char*n)
    if n >=3:
        print(char*n)
        for i in range(n-2):
            print(char," "*(n-4),char)
        print(char*n)

#exercise6
#from array import *
import math
def count_squre_pair(arr):
    """Given an array of numbers, find the number of combination that the sum of two numbers is a perfect square
    
    Parameters
    ------
    arr:array
         
    Returns
    ------
    integer
        return the number of combination
    """
    count=0
    for i in range(len(arr)):
        for j in range(i+1,len(arr)):
            a=int(math.sqrt(arr[i]+arr[j]))
            if a*a==arr[i]+arr[j]:
                count+=1
    return count

