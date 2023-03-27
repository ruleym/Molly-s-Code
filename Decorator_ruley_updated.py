"""Molly Ruley
This program implements retries for a shaky service using decorator functions"""

# import statements
from random import randint
from time import sleep, asctime

"""This is the decorator function with parameters to adjust the values"""
def better_backoff(initial_delay: float, back_off_factor: float, max_delay: float):  # outer decorator to add parameters
    def backoff(func: callable) -> callable:  # inner decorator that returns inner
        delay = 0

        def inner(*args, **kwargs):  # inner function that adds functionality
            nonlocal delay, initial_delay, back_off_factor
            response = func(*args, **kwargs)
            if response != True:
                sleep(delay)  # implements the wait before calling again
                delay *= back_off_factor + initial_delay
                if delay > max_delay:
                    delay = max_delay
                print(f"{asctime()} will be calling after {delay} sec delay\n")
                return False
            if response:
                delay = 0
                print(f"{asctime()} will be calling after {delay} sec delay\n")
                return True
        return inner
    return backoff


""" This decorator shows the result of the call to the service and it adds on to the delay before the next
call should the last call fail"""

@better_backoff(initial_delay=0.1, back_off_factor=1.5, max_delay=2.5)
def call_shaky_service():  # original function
    return 6 == randint(1, 6)


while True:  # calls function
    print(call_shaky_service())
