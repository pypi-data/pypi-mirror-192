# -*- coding: utf-8 -*-

def is_palindrom(num: int) -> bool:
    int_str = str(num)
    if int_str == int_str[::-1]:
        return True

    return False
