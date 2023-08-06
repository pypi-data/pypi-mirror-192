class Calculator:
    """A basic calculator class that supports addition, subtraction, multiplication, division and taking roots."""

    def __init__(self) -> None:
        """Initialize a new Calculator object with a starting value of 0."""
        
        self.value: float = 0

    def __str__(self) -> str:
        """Return the current value of the calculator as a string."""
        return str(self.value)

    def add(self, x: float = 0) -> None:
        """Add a value (x) to the current value of the calculator."""
        try:
            if isinstance(x, (float, int)):
                self.value += x
            else:
                raise ValueError("All values must be numeric!")
        except ValueError as e:
            print(f"Error: {e}")

    def subtract(self, x: float = 0) -> None:
        """Subtract a value (x) from the current value of the calculator."""
        try:
            if isinstance(x, (float, int)):
                self.value -= x
            else:
                raise ValueError("All values must be numeric!")
        except ValueError as e:
            print(f"Error: {e}")

    def multiply_by(self, x: float = 0) -> None:
        """Multiply the current value of the calculator by a given value (x)."""
        try:
            if isinstance(x, (float, int)):
                self.value *= x
            else:
                raise ValueError("All values must be numeric!")
        except ValueError as e:
            print(f"Error: {e}")

    def divide_by(self, x: float = 0) -> None:
        """Divide the current value of the calculator by a given value (x)."""
        try:
            if isinstance(x, (float, int)):
                if x == 0:
                    raise ZeroDivisionError("Can't divide by zero!")
                self.value /= x
            else:
                raise ValueError("All values must be numeric!")
        except ValueError as e:
            print(f"Error: {e}")
        except ZeroDivisionError as e:
            print(f"Error: {e}")

    def take_root(self, x: float = 0) -> None:
        """Take the x-th root of the current value of the calculator."""
        try:
            if isinstance(x, (float, int)):
                if self.value < 0 and x % 2 == 0:
                    raise ValueError("Can't take an even root of a negative number!")
                elif self.value == 0 and x < 0:
                    raise ValueError("Can't take a negative root of zero!")
                else:
                    self.value = self.value ** (1.0/x)
            else:
                raise ValueError("All values must be numeric!")
        except ValueError as e:
            print(f"Error: {e}")

    def set_value(self, x: float = 0) -> None:
        """Set the current value of the calculator to x or clear the calculator's memory."""
        try:
            if isinstance(x, (float, int)):
                self.value = x
            else:
                raise ValueError("All values must be numeric!")
        except ValueError as e:
            print(f"Error: {e}")