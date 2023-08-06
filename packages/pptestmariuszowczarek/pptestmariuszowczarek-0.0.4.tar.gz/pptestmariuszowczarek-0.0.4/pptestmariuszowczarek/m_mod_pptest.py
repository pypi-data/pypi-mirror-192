import numpy as np


def name(first, last):
    """ Return full data of parameters"""
    full = first + " " + last
    full = full.lower().title().strip()
    return 'Witaj: ' + full


def get_np_arr(lst):
    """Returns array of numpy package"""
    return np.array(lst)


if __name__ == '__main__':
    print(name('Mariusz', 'Owczarek'))
    print(get_np_arr([10, 12, 13]))
