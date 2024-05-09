class Rule:
    left: str
    right: str

    def __init__(self, left: str, right: str):
        self.left: str = left
        self.right: str = right
        self.left_boolen_list = [str(i) in left for i in range(10)]
        self.right_boolen_list = [str(i) in right for i in range(10)]

    
    def update(self, right: str | None, left: str | None ) -> None:
        if type(right) == str and (right.isnumeric() or right == '' ):
            self.right = right 
            self.right_boolen_list = [str(i) in right for i in range(10)]
        if type(left) == str and (left.isnumeric() or left == ''):
            self.left = left 
            self.left_boolen_list = [str(i) in left for i in range(10)]