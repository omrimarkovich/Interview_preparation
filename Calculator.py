import typing
from abc import ABC, abstractmethod
from math import sin, cos, tan, log , radians
from typing import Any , Optional


# Constants for actions

BINARY = 0
UNARY = 1


class SimpleCalculator:
    def __init__(self):
        self.__last_result = None

    def calculate(self, *args : Any) -> Any:
        args = list(args)
        action , action_type , args_list = self.input_check(args)
        self.__last_result = action.execute(args_list)
        return self.get_last_result()

    def get_last_result(self):
        if self.__last_result is None:
            raise ValueError("No calculation has been performed yet")
        return self.__last_result

    def input_check(self, args: Any) -> tuple[str , bool , list[int | float]]:
        action_name = args[0]
        action, action_type = ActionsFactory.get_action(action_name)
        if action_type == BINARY:
            list_args = self.val_input(args, action_type)
        elif action_type == UNARY:
            list_args = self.val_input(args, action_type)
        else:
            raise ValueError(f"Action {args[0]} is not supported.")
        return action, action_type , list_args


    def val_input(self, args: Any, action_type : bool ) -> list[float]:
        min_arguments = 2 if action_type == BINARY else 1
        if action_type == UNARY and (len(args) < 1 or len(args) > 2):
            raise TypeError("Unary actions require exactly 1 argument")
        if len(args) == min_arguments:
            args.append(None)
        for ind in range(1,len(args)):
            if args[ind] is None:
                if action_type == BINARY:
                    args[ind-1], args[ind] = self.get_last_result() if ind == 2 else None, args[ind-1]
                else:
                    args[ind] = self.get_last_result() if ind == 1 else None
            elif not isinstance(args[ind] , (int, float)):
                raise TypeError("Unary actions require numeric arguments")
        return args


class BinarActions(ABC):
    @abstractmethod
    def execute(self, args_list: list[int| float]) -> float:
        raise NotImplementedError("This method should be overridden by subclasses")


class UnaryActions(ABC):
    @abstractmethod
    def execute(self, a: float):
        raise NotImplementedError("This method should be overridden by subclasses")


class AddAction(BinarActions):
    def execute(self, args_list: list[int| float]) -> float:
        ans = 0
        for ind in range(1, len(args_list)):
            ans += 0 if args_list[ind] is None else args_list[ind]
        return ans


class SubtractAction(BinarActions):
    def execute(self, args_list: list[int| float]) -> float:
        ans = args_list[1]
        for ind in range(2, len(args_list)):
            ans -= 0 if args_list[ind] is None else args_list[ind]
        return ans


class MultiplyAction(BinarActions):
    def execute(self, args_list: list[int| float]) -> float:
        ans = 1
        for ind in range(1, len(args_list)):
            ans *= 1 if args_list[ind] is None else args_list[ind]
        return ans


class DivideAction(BinarActions):
    def execute(self, args_list: list[int| float]) -> float:
        try:
            ans = args_list[1]
            for ind in range(2, len(args_list)):
                b = 1 if args_list[ind] is None else args_list[ind]
                if b == 0:
                    raise ZeroDivisionError("Cannot divide by zero")
                ans /= b
            return ans
        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero")


class PowerAction(BinarActions):
    def execute(self, args_list: list[int| float]) -> float:
        ans = args_list[1]
        for ind in range(2, len(args_list)):
            ans **= 1 if args_list[ind] is None else args_list[ind]
        return ans



class RootAction(BinarActions):
    def execute(self, args_list: list[int| float]) -> float:
        ans = args_list[1]
        if ans < 0:
            raise ValueError("Cannot calculate square root of a negative number")
        for ind in range(2, len(args_list)):
            b = 1 if args_list[ind] is None else args_list[ind]
            if b <= 0:
                raise ValueError("Root degree must be a positive number")
            ans = ans ** (1 / b)
        return ans


class SinAction(UnaryActions):
    def execute(self, args_list: list[int| float]) -> float:
        try:
            return sin(radians(args_list[1]))
        except ValueError :
            raise ValueError("Invalid input for sine function, must be a number ")


class CosAction(UnaryActions):
    def execute(self, args_list: list[int| float]) -> float:
        try:
            return cos(radians(args_list[1]))
        except ValueError:
            raise ValueError("Invalid input for cosine function, must be a number ")

class TanAction(UnaryActions):
    def execute(self, args_list: list[int| float]) -> float:
        return tan(radians(args_list[1]))


class LogAction(UnaryActions):
    def execute(self, args_list: list[int| float]) -> float:
        if args_list[1] <= 0:
            raise ValueError("Logarithm is undefined for non-positive numbers")
        return log(args_list[1])


class ActionsFactory:
    actions = {
        "add": (AddAction(), BINARY),
        "subtract": (SubtractAction(), BINARY),
        "multiply": (MultiplyAction(), BINARY),
        "divide": (DivideAction(), BINARY),
        "power": (PowerAction(), BINARY),
        "root": (RootAction(), BINARY),
        "sin": (SinAction(), UNARY),
        "cos": (CosAction(), UNARY),
        "tan": (TanAction(), UNARY),
        "log": (LogAction(), UNARY),
    }

    @classmethod
    def get_action(cls, action_name: str) -> tuple[BinarActions, int] | tuple[UnaryActions, int] | tuple[None, None]:
        if action_name.lower() in cls.actions:
            return cls.actions[action_name.lower()]
        return None, None
