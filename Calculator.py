import typing
from abc import ABC, abstractmethod
from math import sin , cos, tan, log



class SimpleCalculator :
    def __init__(self):
        self.__last_result = None

    def calculate(self, act: str ,a : float , b = None) -> float:
        action = ActionsFactory.get_action(act)
        if action is None:
            raise ValueError(f"Action {act} is not supported")
        if b is None:
            b = a
            a = self.__last_result
        self.__last_result = action.execute(a, b)
        return self.get_last_result()

    def get_last_result(self):
        if self.__last_result is None:
            raise ValueError("No calculation has been performed yet")
        return self.__last_result


class MathActions(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        raise NotImplementedError("This method should be overridden by subclasses")

class AddAction(MathActions):
    def execute(self, a: float, b: float) -> float:
        return a + b

class SubtractAction(MathActions):
    def execute(self, a: float, b: float) -> float:
        return a - b

class MultiplyAction(MathActions):
    def execute(self, a: float, b: float) -> float:
        return a * b

class DivideAction(MathActions):
    def execute(self, a: float, b: float) -> float:
        try:
            return a / b
        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero")

class PowerAction(MathActions):
    def execute(self, a: float, b: float) -> float:
        return a ** b

class RootAction(MathActions):
    def execute(self, a: float, b: float = None) -> float:
        if a < 0:
            raise ValueError("Cannot calculate square root of a negative number")
        return a ** (1/b)


class ActionsFactory:
    actions = {
        "add": AddAction(),
        "subtract": SubtractAction(),
        "multiply": MultiplyAction(),
        "divide": DivideAction(),
        "power": PowerAction(),
        "root": RootAction()
    }

    @classmethod
    def get_action(cls, action_name: str) -> typing.Optional[MathActions]:
        if action_name.lower() in cls.actions:
            return cls.actions[action_name.lower()]
        return None



