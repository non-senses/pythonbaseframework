

def addNameToList(name, list = []):
    list.append(name)
    return list

print(addNameToList('First Name'))
print(addNameToList('Second Name'))
print(addNameToList('Fourth Name',  ['Fifth name']))

print("** ")
print(" Watch out with mutable function arguments!")
print("** ")


if (False):
    def addNameToListInPython(name, list = None):
        if list is None:
            list = []

        list.append(name)
        return list

    print(addNameToListInPython('First Name'))
    print(addNameToListInPython('Second Name'))
    print(addNameToListInPython('Fourth Name',  ['Fifth name']))

"""
Function parameters are read and interpreted only ONCE when parsing the file
"""

