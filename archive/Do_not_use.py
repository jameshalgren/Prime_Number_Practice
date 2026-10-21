import numpy as np
import math
# needs to input three things, a number for width, a number for max value, and a starting integer
# the starting integer is a creative liberty because he said it was a list of functions from my understanding.


def create_list_of_values(max_value, start):
    return list(range(start, max_value + 1))

def create_initial_primes(num_list):
    not_1 = False
    i = 0
    primes = []
    while not not_1:
        if num_list[i] > 1:
            primes.append(num_list[i])
            not_1 = True
        i += 1
    return primes, i


def remove_multiples(num_list):
    

    # what the AI came up with, which is a bit more efficient than the one I came up with, but I think mine is easier to understand, and I think it is more efficient than the one he came up with, but I am not sure about that.
    # I kept the line above because the AI in VS code wrote it for me and I thought it was funny how it basically called itself smarter than me, even tho its true it is hilarious
    if not num_list:
        return num_list
    primes, i = create_initial_primes(num_list)
    for num in num_list[i:]:
        is_prime = True
        for prime in primes:
            if prime * prime > num:
                break
            if num % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    # print(primes) #for testing/comment out later
    return primes


def display_list(num_list, width):
    # use nup.reshape(data, (-1,width)) to display the data where -1 means figure out the rows for me.

    if len(num_list) % width != 0:
        # then add zeros as place holders
        length = len(num_list)
        rounded = (math.ceil(length / width) * width)
        r = rounded - length
        for i in range(r):
            num_list.append(0)
    num_a = np.array(num_list)
    num_array = np.reshape(num_a, (-1, width))
    print(num_array)

def find_primes(width, max_value, start):
    num_list = create_list_of_values(max_value, start)
    upd_list = remove_multiples(num_list)
    # print(upd_list)
    display_list(upd_list, width)

def get_values():
    try:
        print('Let\'s proceed:')
        width = int(input('Please enter the width: '))
        max_value = int(input('Please enter the maximum number: '))
        start = int(input('Please enter the starting number: '))
    except ValueError:
            print('Please enter a whole number and try again')
            return None, None, None
    return width, max_value, start

def main():
    print('Welcome to the Hydroinformatics Lab!')
    print('Today we will test this idea with numbers but if you would like to try functions or something more advanced,'
          '\nthen there is a version without the terminal interaction.')
    while True:
        width, max_value, start = get_values()
        find_primes(width, max_value, start)
        cont = input('Would you like to continue? (y/n) ')
        if cont == 'n':
            print('Happy Easter! He is Risen!!!')
            break

if __name__ == '__main__':
    main()
