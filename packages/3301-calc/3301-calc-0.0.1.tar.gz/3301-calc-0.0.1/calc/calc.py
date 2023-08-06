# -*- coding: utf-8 -*-

"""Some Comment"""

from .odd import is_odd, is_even
from .prime import is_prime
from .palindrom import is_palindrom


def main():
    while True:
        print("\nEnter 0 to quit")
        print("Enter 1 to check odd")
        print("Enter 2 to check even")
        print("Enter 3 to check prime")
        print("Enter 4 to check palindrom")
        ch = int(input("Enter choice: "))
        if ch == 0:
            exit(0)

        num = int(input("Enter a number: "))

        if ch == 1:
            print(f"Number {num} {'is' if is_odd(num) else 'is not'} odd")
        elif ch == 2:
            print(f"Number {num} {'is' if is_even(num) else 'is not'} even")
        elif ch == 3:
            print(f"Number {num} {'is' if is_prime(num) else 'is not'} prime")
        elif ch == 4:
            print(f"Number {num} {'is' if is_palindrom(num) else 'is not'} palindrom")
        else:
            print("Invalid input")
