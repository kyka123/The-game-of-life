from models.rule import Rule

class BuiltInObject:
    def __init__(self, object_matrix: list[list[int]], prefer_rule: Rule, name: str):
        self.object_matrix: list[list[bool]] = object_matrix
        self.width: int = len(object_matrix[0])
        self.height: int = len(object_matrix)
        self.prefer_rule: list[list[bool]] = prefer_rule
        self.name: str = name

