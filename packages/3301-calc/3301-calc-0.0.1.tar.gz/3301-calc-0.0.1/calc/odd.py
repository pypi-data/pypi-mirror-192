# -*- coding: utf-8 -*-

def is_odd(num: int) -> bool:
    if num % 2 != 0:
        return True
    else:
        return False


def is_even(num: int) -> bool:
    return not is_odd(num)
