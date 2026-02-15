import numpy as np

class InvalidInputError(Exception):
    pass

type_option = np.array(['sine', 'square', 'saw', 'triangle'])

def testDict(type):
    try:
        if(type in type_option):
            return True
        else:
            raise InvalidInputError('Type must be sine, square, saw, or triangle')
    except InvalidInputError as e:
        return e

print(testDict('noise'))
print(testDict('sine'))