import numpy

def name(first, last):
    """"Returns full data of parameters"""

    full = first + " " + last
    return "Welcome: " + full

def get_numpy_arr(lst):
    """"Returns array of numpy package"""

    return numpy.array(lst)
if __name__ == "__main__":
    print(name("Szymon", "Radosz"))
    print(get_numpy_arr([1, 2, 3, 4, 5]))

