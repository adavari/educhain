from random import randint


def is_valid_number(num: str):
    if num[0] != '0':
        return False
    if len(num) != 11:
        return False

    return True


def num_to_sabacell_num(num: str):
    return '98' + num[1:]


def random_digit():
    range_start = 10 ** (4 - 1)
    range_end = (10 ** 4) - 1
    return randint(range_start, range_end).__str__()
