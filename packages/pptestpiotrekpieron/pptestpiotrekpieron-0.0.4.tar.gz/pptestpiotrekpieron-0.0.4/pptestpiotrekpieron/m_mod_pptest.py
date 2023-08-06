import numpy


def name(fname, lname):
    """Returns full data of parameters"""
    full = fname + " " + lname
    full = full.lower().title().strip()

    return "Witaj: " + full


def get_numpy_arr(lst):
    """Returns array of numpy package"""

    return numpy.array(lst)


if __name__ == "__main__":
    print(name('Adrian', "Zapala"))
    print(get_numpy_arr([1, 2, 3, 4, 5]))