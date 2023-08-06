# -*- coding: utf-8 -*-

def is_prime(num: int) -> bool:
    for i in range(2, num):
        if num % i == 0:
            return False

    return True
