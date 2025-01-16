from collections.abc import Callable

class Option:
    name: str
    action: Callable

    def __init__(self, name: str, action: Callable):
        self.name = name
        self.action = action
