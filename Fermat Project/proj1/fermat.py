import random
import numpy as np

def prime_test(N, k):
	# This is main function, that is connected to the Test button. You don't need to touch it.
	return fermat(N,k), miller_rabin(N,k)


def mod_exp(x, y, N):
    # You will need to implement this function and change the return value.   
    if y == 0:
        return 1
    z = mod_exp(x, np.floor(y/2), N)
    if y % 2 == 0:
        return np.square(z) % N
    else:
        return (x * np.square(z)) % N
	

def fprobability(k):
    # You will need to implement this function and change the return value.   
    return 1- 1/(2**k)


def mprobability(k):
    # You will need to implement this function and change the return value.   
    return 1 - 1/(4**k)


def fermat(N,k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
	#
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
    numbers = []
    for i in range(k):
        number = random.randint(1, N-1)
        while number in numbers:
            number = random.randint(1, N-1)
        numbers.append(number)
    for j in numbers:
        if mod_exp(j, N-1, N) != 1:
            return 'composite'
    return 'prime'


def miller_rabin(N,k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
	#
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
    numbers = []
    for i in range(k):
        number = random.randint(1, N-1)
        while number in numbers:
            number = random.randint(1, N-1)
        numbers.append(number)
    for j in numbers:
        if mod_exp(j, N-1, N) != 1:
            return 'composite'
        else:
            newNum = (N-1)/2
            while(mod_exp(j, newNum, N) == 1):
                if newNum % 2 == 0:
                    newNum = newNum/2
                else:
                    break
            if mod_exp(j, newNum, N) != N-1 and mod_exp(j, newNum, N) != 1:
                return 'composite'
    return 'prime'