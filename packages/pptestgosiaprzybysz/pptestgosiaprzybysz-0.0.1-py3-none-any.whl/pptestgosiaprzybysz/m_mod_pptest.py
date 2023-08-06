import numpy


def name(first, last):
    """returns full data of parameters"""

    full = first + " " + last
    return "Witaj: " + full


def get_numpy_arr(lst):
    """returns array of numpy package"""

    return numpy.array(lst)


if __name__ == "__main__":
    print(name("Adrian", "Zapala"))
    print(get_numpy_arr([1, 2, 3, 4, 5, 6]))
