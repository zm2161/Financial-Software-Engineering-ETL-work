from collections import Counter
import sys


def tuple_types(input_tuple):
    """ Checks element types in tuple
    param input_tuple: tuple
        object tuple to traverse/type check
    return: tuple or str
        tuple of data types; str if the input was not a tuple itself
    """
    list_of_types = []
    if isinstance(input_tuple, tuple):
        for element in input_tuple:
            list_of_types.append(type(element))
        return tuple(list_of_types)
    else:
        return "Parameter must be a tuple"


def remove_element(input_tuple, element):
    """ This function drops the specified element
    param input_tuple: tuple
        object to remove element from
    param element: varying
        element of varying type to remove
    return: tuple
        returns tuple without the element specified
    """
    return tuple(item for item in input_tuple if item != element)


def check_containment(input_string, lookup_string):
    # ask Serge/Sheeran if this is to check for enough letters to make substring or the substring
    # must be all together
    """ Function checks if input_string has enough letters to
        construct lookup_string
    param input_string: str
        phrase containing letters available to
        lookup_string
    param lookup_string: str
        phrase to check in input_string counts
    return: bool
        True if input_string has enough letters for lookup_string;
        False otherwise
    """
    dict_input_string = Counter(input_string)
    dict_lookup_string = Counter(lookup_string)

    for k, v in dict_lookup_string.items():
        if dict_input_string[k] < dict_lookup_string[k]:
            return False
    return True


def reverse(input_string):
    """ Reverses input_string
    param input_string: str
        phrase to reverse
    return: str
        returns reversed input_string
    """
    return input_string[::-1]


def concatenate(list1, list2):
    # can we assume that elements of lists are homogenous and can be added (e.g., can't be dict or set)
    # and that lists are of equal length
    """ Concatenates list1 and list2 by index
    param list1: list
        first list to combine with list2
    param list2: list
        second list to combine with list1
    return: list
        result of index-based concatenation
    """
    a_list = []
    for first_element, second_element in zip(list1, list2):
        a_list.append(first_element + second_element)
    return a_list


def concatenate_list_of_lists(input_list):
    # this assumes all internal lists are of equal length and homogenous datatypes at each column
    # and that all lists are of equal size
    """ Concatenates embedded lists of a passed list by index
    param input_list: list of lists
        a list of lists to concatenate
    return: list
        resulting list with index-based concatenation of all
        embedded lists in input_list
    """
    list1 = input_list[0]
    list2 = input_list[1]
    return concatenate(list1, list2)


# Note: _list was added to function signature to avoid
#       confusion with tuple remove_element method.
def remove_element_list(input_list, element):
    """ Removes specified element from input_list
    param input_list: list
        source list
    param element: various
        element to remove from list
    return: list
        resulting list without specified element
    """
    input_list.remove(element)
    return input_list


def deep_copy(input_list):
    # should deep copy have differing id() for primitive and non-primitives?
    # should we assume potentially infinite embedded non-primitives?
    """ Creates deep copy of input_list
    param input_list: list
        original list to deep copy
    return: list
        new list object with deep copy characteristics
    """
    def return_copy_by_instance(object_to_copy, object_idx):
        """ Helper function to handle various data types
        param object_to_copy: various
            object to copy
        param object_idx: int
            index of current object
        return: various
            returns appropriate object based on object_to_copy
        """
        if isinstance(object_to_copy, primitives):
            return element
        elif isinstance(object_to_copy, dict):
            new_dict = {}
            for k, v in object_to_copy.items():
                new_dict[k] = v
            return new_dict
        elif isinstance(object_to_copy, set):
            new_set = set()
            for item in object_to_copy:
                new_set.add(item)
            return new_set
        elif isinstance(object_to_copy, tuple):
            new_tuple = ()
            for item in object_to_copy:
                new_tuple += (item,)
            return new_tuple
        else:
            return f"Unrecognized object type at {object_idx}"

    primitives = (int, float, str, bool)
    deep_copy_list = []
    for idx, element in enumerate(input_list):
        deep_copy_list.append(return_copy_by_instance(element, idx))
    return deep_copy_list


def find(input_dict):
    # does this need to find all the keys or a specified one? Function sig in ppt doesn't have a key parameter to
    # specify also, if an outer dict shares a key with an inner dict, do we just create one overall key with its
    # values no matter the level?
    """ Finds all values by key in tuple format
    param input_dict: dict
        dictionary to traverse
    return: tuple
        resulting tuple outlining the values for each key
    """
    tuple_to_return = ()
    for k, v in input_dict.items():
        # Note: recursion to handle dict of dicts
        if isinstance(v, dict):
            tuple_to_return += ((k, find(v)),)
        else:
            tuple_to_return += ((k, v),)
    return tuple_to_return


def min_value(input_dict):
    """ Returns key of minimum value in input_dict
    param input_dict: dict
        dictionary to traverse
    return: various
        returns key corresponding to minimum value
    """
    running_min = sys.maxsize
    # Note: dictionary used to accommodate various types of key types
    variable_storage = {}
    for k, v in input_dict.items():
        if v < running_min:
            variable_storage['min_key'] = k
            running_min = v
    return variable_storage['min_key']


if __name__ == '__main__':
    print('Testing tuple_types')
    print(tuple_types((1, 'hello', [], {}, set())))
    print((1, 'hello', [], {}, set()))
    print()

    print('Testing remove_element')
    list_to_remove = [1, 2, 3]
    dict_to_remove = {1: 2, 3: 4}
    set_to_remove = (1, 'hello', [], {}, set())
    test = (1, 'hello', list_to_remove, dict_to_remove, set_to_remove)
    print(remove_element(test, 'hello'))
    print(remove_element(test, 1))
    print(remove_element(test, list_to_remove))
    print(remove_element(test, dict_to_remove))
    print(remove_element(test, set_to_remove))
    print()

    print('Testing check_containment')
    print(check_containment('mississippi', 'sipped'))
    print(check_containment('mississippi', 'sipp'))
    print(check_containment('mississippi', 'mississippis'))
    print()

    print('Testing reverse')
    print(reverse("killer robots are too unfriendly"))
    print(reverse(reverse("killer robots are too unfriendly")))
    print()

    print('Testing concatenate')
    print(concatenate([1, 2, 3, 4], [1, 2, 3, 4]))
    print(concatenate(["I'm ", "You're ", 1, 2], ["Dennis", "not Dennis", 1, 2]))
    print(concatenate([[1], [2]], [[1], [2]]))
    print()

    print('Testing concatenate_list_of_lists')
    print(concatenate_list_of_lists([[1, 2, 3, 4], [1, 2, 3, 4]]))
    print(concatenate_list_of_lists([["I'm ", "You're ", 1, 2], ["Dennis", "not Dennis", 1, 2]]))
    print()

    print('Testing remove_element_list')
    print(remove_element_list([1, 2, 3, 4], 2))
    test_dct = {}
    print(remove_element_list([1, 'hello', test_dct, 4], test_dct))
    print()

    print('Testing deep_copy')
    test_tuple = (4, 'what what')
    test_dict = {2: 'world'}
    test_set = {1, 2, 4}
    test_list = [1, 'string', test_tuple, test_dict, test_set]
    copy_list = deep_copy(test_list)

    print(f'test_list looks like: {test_list}')
    print(f'copy_list looks like: {copy_list}')
    print()
    print(f'my implementation types: {[type(item) for item in copy_list]}')
    print(f'original types: {[type(item) for item in copy_list]}')

    for i in range(len(test_list)):
        print(id(test_list[i]) == id(copy_list[i]))
    print()

    print('Testing find')
    test_dict = {'L1K1': 2, 'L1K2': 4,
                 'L1K3': {'L2K1': 7,
                          'L2K2': {'L3K1': 10,
                                   'L3K2': 12}}}
    print(test_dict)
    print(find(test_dict))
    print()

    print('Testing min_value')
    test_dict1 = {'first': 1, 'second': -3243123.045, 'third': 21873649}
    test_dict2 = {'first': 1, 'second': 3243123.045, 'third': 21873649}
    test_dict3 = {'first': -1, 'second': -3243123.045, 'third': -21873649}
    test_dict4 = {1: -1, 2: -3243123.045, 3: -21873649}
    print(min_value(test_dict1))
    print(min_value(test_dict2))
    print(min_value(test_dict3))
    print(min_value(test_dict4))
