
from abc import ABC, abstractmethod
from math import sin, cos, tan, log , radians
from typing import Any , Optional , Union


# Constants for actions

BINARY = 0
UNARY = 1

# Messages for user
INPUT_MESSAGE = "Insert the action and arguments separated by spaces.\n you can Exit anytime by click 'e' butten \n"
EXIT_MESSAGE = "Exiting the calculator.\n"
CONTINUE_MESSAGE = "Press Enter to continue or 'e' to exit: \n"
CONFIRMATION_MESSAGE = "Confirm your input. Write 'yes' to confirm \n"

class SimpleCalculator:

    EXCEPTION_MESSAGE = "An error occurred during th calculation. return the last result: \n"

    def __init__(self):
        self.__last_result = None

    def calculate(self, action_name : str,  *args : Optional[str]) -> Any:
        try:
            action, action_type = ActionsFactory.get_action(action_name)
            self.input_check(*args)
            args = self.add_last_result(action_type ,*args)
            self.__last_result = action(*args)
        except (ValueError , TypeError , ZeroDivisionError)  as e:
            print(e ,"\n", self.EXCEPTION_MESSAGE)
        except Exception as e:
            print(f"An unexpected error occurred: {e}" , "\n", self.EXCEPTION_MESSAGE)
        finally:
            return self.get_last_result()

    def get_last_result(self):
        if self.__last_result is None:
                print("No calculation has been performed yet \n")
                return None
        return self.__last_result

    def input_check(self, *args: Optional[str]) -> None:
        for arg in args:
            if arg is None or not arg.isnumeric():
                raise TypeError("Unary actions require numeric arguments")

    def add_last_result(self, action_type : bool , *args: Optional[str]) -> tuple[Optional[str]]:
        min_argument = 1 if action_type else 0
        if len(args) == min_argument  : # todo: fix when there is a none in the second place
            args = (self.get_last_result()) + args
        elif args[0] is None:
            args = (self.get_last_result()) + args[1:]
        return args


class BinaryAction(ABC):
    MIN_ARGUMENTS = 2
    @abstractmethod
    def __call__(self, *args : Optional[str]) -> float:
        raise NotImplementedError("This method should be overridden by subclasses")

    @classmethod
    def argument_check(cls ,  *args : Optional[str]) -> None:
        if len(args) < cls.MIN_ARGUMENTS:
            raise ValueError("At least two arguments are required for binary actions")


class UnaryActions(ABC):
    MAX_ARGUMENTS = 1
    @abstractmethod
    def __call__(self, a: float):
        raise NotImplementedError("This method should be overridden by subclasses")

    @classmethod
    def argument_check(cls ,  *args : Optional[str]) -> None:
        if len(args) > cls.MAX_ARGUMENTS:
            raise TypeError("Unary actions require at most 1 argument")


class AddAction(BinaryAction):
    def __call__(self,  *args : Optional[str]) -> float:
        ans = 0
        for ind in range(len(args)):
            ans += 0 if args[ind] is None else float(args[ind])
        return ans


class SubtractAction(BinaryAction):
    def __call__(self,  *args : Optional[str]) -> float:
        ans = float(args[0])
        for ind in range(len(args)):
            ans -= 0 if args[ind] is None else float(args[ind])
        return ans


class MultiplyAction(BinaryAction):
    def __call__(self,  *args : Optional[str]) -> float:
        ans = 1
        for ind in range(len(args)):
            ans *= 1 if args[ind] is None else float(args[ind])
        return ans


class DivideAction(BinaryAction):
    def __call__(self,  *args : Optional[str]) -> float:

        ans = float(args[0])
        for ind in range(len(args)):
            b = 1 if args[ind] is None else float(args[ind])
            if b == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            ans /= b
        return ans



class PowerAction(BinaryAction):
    def __call__(self,  *args : Optional[str]) -> float:
        ans = float(args[0])
        for ind in range(len(args)):
            ans **= 1 if args[ind] is None else float(args[ind])
        return ans



class RootAction(BinaryAction):
    def __call__(self,  *args : Optional[str]) -> float:
        ans = float(args[0])
        if ans < 0:
            raise ValueError("Cannot calculate square root of a negative number")
        for ind in range(2, len(args)):
            b = 1 if args[ind] is None else float(args[ind])
            if b <= 0:
                raise ValueError("Root degree must be a positive number")
            ans = ans ** (1 / b)
        return ans


class SinAction(UnaryActions):
    def __call__(self,   *args : Optional[str]) -> float:
            return sin(radians(float(args[0])))



class CosAction(UnaryActions):
    def __call__(self,  *args : Optional[str]) -> float:
            return cos(radians(float(args[0])))


class TanAction(UnaryActions):
    def __call__(self,  *args : Optional[str]) -> float:
        return tan(radians(float(args[0])))


class LogAction(UnaryActions):
    def __call__(self, args_list: list[int| float]) -> float:
        if args_list[0] <= 0:
            raise ValueError("Logarithm is undefined for non-positive numbers")
        return log(float(args_list[0]))


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
    def get_action(cls, action_name: str) -> tuple[BinaryAction, int] | tuple[UnaryActions, int] | tuple[None, None]:
        if action_name.lower() in cls.actions:
            return cls.actions[action_name.lower()]
        raise ValueError(f"Action {action_name} is not supported.")


def main(*args):
    calc = SimpleCalculator()
    while True:
        user_input = input(INPUT_MESSAGE).split()
        if user_input[0].lower() == "e":
            print(EXIT_MESSAGE)
            break
        print("You entered:", user_input,"\n", )
        confirmation = input(CONFIRMATION_MESSAGE).strip().lower()
        if confirmation != 'yes':
            print("Input not confirmed, please try again.")
            continue
        print("Calculating...")
        print ("Your result:\n" , calc.calculate(*user_input))
        user_input = input(CONTINUE_MESSAGE)
        if user_input.lower() == 'e':
            print(EXIT_MESSAGE)
            break






if __name__ == "__main__":
    main()
