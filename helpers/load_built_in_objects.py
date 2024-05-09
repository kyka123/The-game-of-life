from io import TextIOWrapper

from models.built_in_object import BuiltInObject
from models.rule import Rule

BUILT_IN_OBJECTS_PATH = 'assets/built_in_objects.txt'

def load_buit_in_objects() -> list[BuiltInObject]:
    file: TextIOWrapper = open(BUILT_IN_OBJECTS_PATH, 'r')
    objects: BuiltInObject = []
    object_name: str | None = None
    object_rule: str | None = None
    object_matrix: str | None = None

    for line in file:
        line = line.rstrip()
        if line == '-':
            if object_name == None or object_rule == None or object_matrix == None:
                raise Exception("built_in_objects.txt file is incorrect")
            else:
                objects.append(BuiltInObject(object_matrix=object_matrix, prefer_rule=object_rule, name=object_name))
                object_name = None
                object_rule = None
                object_matrix = None

        elif object_name == None:
            object_name = line
        elif object_rule == None:
            l, r = line.split('/')
            object_rule = Rule(l, r)
        else:
            if object_matrix == None:
                object_matrix = []
            object_matrix.append(list(map(int, [*line])))
    file.close()
    return objects
