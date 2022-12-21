#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 00:00:00 2022

@author: Nick Lewis
"""


class StructuredDict:
    def __init__(self, d):
        self.__check(d)
        self.__d = d

    def __str__(self):
        return str(self.__d)

    def __repr__(self):
        return repr(self.__d)

    def __len__(self):
        return len(self.__d)

    def __contains__(self, item):
        return item in self.__d

    def __iter__(self):
        for k in self.__d:
            yield k
        
    def __getitem__(self, key):
        return self.__d[key]

    def __delitem__(self, key):
        raise DeleteError()

    def __setitem__(self, key, value):
        if type(value) is not self.__class__.key_to_type[key]:
            raise UpdateValueError(key, value, self.__class__.key_to_type[key])
        self.__d[key] = value

    def __check(self, d):
        # keys that are missing from d;
        # additional keys that d has;
        # the keys in d associated with a type error.
       
        missing = set()
        additional = set()
        type_error = set()
        keys = set(self.__class__.key_to_type.keys())
        dict_keys = set(d.keys())
    
        missing = keys - dict_keys
        additional = dict_keys - keys
        dict_keys -= additional
   
        to_raise = False
   
        for key in dict_keys:
            if type(d[key]) != self.__class__.key_to_type[key]:
                type_error.add(key)    
                to_raise = True
                
        if missing != set() or additional != set():
            to_raise = True
        
        if to_raise:    
            raise InitializationError(d, self.__class__.key_to_type, missing, additional, type_error)

            


class StructuredDictError(Exception):
    pass

class DeleteError(StructuredDictError):
    def __str__(self):
        return 'You cannot delete from a StructuredDict'

class UpdateValueError(StructuredDictError):
    def __init__(self, key, value, key_to_type):
        self.key = key
        self.value = value
        self.key_to_type = key_to_type
    
    def __str__(self):
        L = "The type of " + repr(self.value) + " is " + str(type(self.value))
        L += ", but the value corresponding to the key " + repr(self.key)
        L += " should have type " + str(self.key_to_type)
        return L


class InitializationError(StructuredDictError):
    def __init__(self, d, key_to_type, mis, add, typ):
        self.d = d
        self.key_to_type = key_to_type
        self.mis = mis
        self.add = add
        self.typ = typ
    
    def __str__(self):
        Missing = ''
        Added = ''
        if self.mis != set():
            Missing = 'the following keys are missing from d: ' + str(self.mis) + ';\n'
        
        if self.add != set():
            Added = 'the following keys were supplied in error: ' + str(self.add) + ';\n'
        Type_Err = ''
        for el in self.typ:
            Type_Err += 'the type of d[' + repr(el) + '] is ' + str(type(self.d[el]))
            Type_Err += ', but it should be ' + str(self.key_to_type[el]) + ';\n'
        Type_Err = Type_Err[:-2]
        #Deletes extra last new line
        return Missing + Added + Type_Err


class Rectangle(StructuredDict):
    key_to_type = {'len1': float, 'len2': float}

    def __init__(self, len1, len2):
        d = {'len1' : len1, 'len2' : len2}
        super().__init__(d)

    def area(self):
        return self['len1'] * self['len2']


class Student(StructuredDict):
    key_to_type = {'first name': str, 'last name': str, 'GPA': float}

    def __init__(self, first, last, gpa):
        d = {'first name': first, 'last name': last, 'GPA': gpa}
        super().__init__(d)

    def __str__(self):
        name = 'Name: ' + self['first name'] + ' ' + self['last name'] + ', '
        gpa = 'GPA: ' + str(self['GPA'])

        return name + gpa



if __name__ == '__main__':
    r = Rectangle(2.0, 4.0)
    print('area =', r.area())

    def f1():
        r = Rectangle(2.0, 4.0)
        del r['len1']

    def f2():
        r = Rectangle(2.0, 4.0)
        r['len1'] = 2

    def f3():
        r = Rectangle(2, '4')
        return r

    def f4():
        class C(StructuredDict):
            key_to_type = {0:int, 1:int, 2:int, 3:float, 4:str}

        c = C({2:2, 3:3, 4:4, 5:5, 6:6})
        return c
    
    L = [f1, f2, f3, f4]

    for f in L:
        try:
            print('')
            f()
        except DeleteError as e:
            print('DeleteError:', e)
        except UpdateValueError as e:
            print('UpdateValueError:', e)
        except InitializationError as e:
            print('InitializationError:', e)


# MY OUTPUT
# area = 8.0

# DeleteError: You cannot delete from a StructuredDict

# UpdateValueError: The type of 2 is <class 'int'>, but the value corresponding to the key 'len1' should have type <class 'float'>

# InitializationError: the type of d['len1'] is <class 'int'>, but it should be <class 'float'>;
# the type of d['len2'] is <class 'str'>, but it should be <class 'float'>;

# InitializationError: the following keys are missing from d: {0, 1};
# the following keys were supplied in error: {5, 6};
# the type of d[3] is <class 'int'>, but it should be <class 'float'>;
# the type of d[4] is <class 'int'>, but it should be <class 'str'>;

