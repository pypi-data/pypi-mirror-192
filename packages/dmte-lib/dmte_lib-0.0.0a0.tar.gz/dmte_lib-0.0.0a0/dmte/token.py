from typing import Tuple


class Token:
    def __init__(self, type_: Tuple, str_value: str):
        self.type_ = type_
        self.str_value = str_value

    def as_tuple(self):
        return self.type_, self.str_value

    def __str__(self):
        return str(self.as_tuple())
