import numpy

def name(first, last):
    '''Returns full data of parameters'''

    full = first + " " + last
    full = full.lower().title().strip()
    return "Witaj: " + full


def get_numpy_arr(lst):
    """Retuns array of numpy package"""
    return numpy.array(lst)

if __name__ == "__main__":
    print(name("Marcin","Siatkowski"))
    print(get_numpy_arr([1,2,3,4,5]))