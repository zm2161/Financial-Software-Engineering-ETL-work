def  tuple_types(input_tuple):
    """
    Checks every element of given tuple and reports back on its type
    Params
    input_tuple:tuple

    Return
    tuple of types
    """
    output=()
    for input in input_tuple:
        output=output+(type(input),)
    return output


def remove_element(input_tuple, element):
    """
    Removes an element from given tuple; function returns resulted tuple
    Params
    input_tuple:tuple
    element

    Return
    tuple
    """
    output=()
    for input in input_tuple:    
        if element !=input:
            output=output+(input,)
    return output

def check_containment(input_string, lookup_string):
    """
    Checks for substring availability in given string; function returns bool value
    Params
    input_string:string
    lookup_string:string

    Return
    bool
    """
    if lookup_string in input_string:return True
    else: return False
def reverse(input_string):
    """
    Removes an element from given tuple; function returns resulted tuple
    Params
    input_string:str

    Return
    str
    """
    return input_string[::-1]


def concatenate(list1, list2):
    """
    Concatenates two lists index-wise; function returns resulted list
    Params
    list1:list
    list2:list

    Return
    list
    """
    output=list (zip(list1,list2))
    return output


def concatenate_list_of_lists(input_list):
    """
    Argument to the function is the list of lists; 
    concatenate all list elements index-wise; function returns resulted lis
    Params
    input_list:list of lists

    Return
    list
    """
    output=list(zip(*input_list))
    return output


def remove_element_list(input_list, element):
    """
    Removes an element from given list; function returns resulted list
    Params
    input_list:list
    element

    Return
    list
    """
    try:
        input_list.remove(element)
        return input_list
    except ValueError:
        print("Error: element not in list")
        
def deep_copy(input_list):
    """
    deep copy of given list
    Params
    input_list:list

    Return
    list
    """
    from copy import deepcopy
    deep=deepcopy(input_list)
    print('new copy the same as before ? ', deep is input_list)
    return deep


def find(input_dict,element):
    """
    find all elements with specified key; make sure to account for the case where given dictionary is a dict of dicts; 
    this function should traverse all elements of inner dict elements; 
    function returns resulted tuple of key, value pairs or such elements
    Params
    input_dict:dict
    element

    Return
    tuple
    """
    output=()
    
    for k,v in input_dict.items():
        if k==element:
            output=output+(k,v),
        if isinstance(v, dict):
            
            results=find(v,element)
            # for result in results:
            #     print(type(result))
            #     output=output+(result,)
        
    return output

def min_value(input_dict):
    """
    Returns the key, corresponding to the min value from given dictionary
    Params
    input_dict:dict

    Return
    string/int/float
    """
    return min(input_dict,key=input_dict.get)
    
    

print(tuple_types(("Tango", 100.32, 25, True)))
print(remove_element( (100.32, 25, True),True))
print(check_containment('I like you', 'youi'))
print(reverse('cbd'))
print(concatenate([1,2], [3,4]))
l = [[1,2], [3,4]]
print(concatenate_list_of_lists(l))
print(remove_element_list([1,2,3], 4))
print(remove_element_list([1,2,3], 3))
print(deep_copy([1,2,3]))
print(find({'a':{'a':(1,2)},'b':1,'a':3},'a'))
print(min_value({'a': 10, 'b': 20, 'c': 5}))