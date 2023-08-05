class Calculator:
    """A basic calculator class that supports addition, subtraction, multiplication, division and taking roots."""

    def __init__(self) -> None:
        """Initialize a new Calculator object with a starting value of 0."""
        self.value: float = 0

    def add(self, x: float) -> None:
        """Add a value (x) to the current value of the calculator"""
        self.value += x

    def subtract(self, x: float) -> None:
        """Subtract a value (x) from the current value of the calculator."""
        self.value -= x

    def multiply_by(self, x: float) -> None:
        """Multiply the current value of the calculator by a given value (x)."""
        self.value *= x

    def divide_by(self, x: float) -> None:
        """Divide the current value of the calculator by a given value (x)."""
        self.value /= x

    def take_root(self, x: float) -> None:
        """Take the x-th root of the current value of the calculator."""
        self.value = self.value ** (1.0/x)

    def reset_memory(self) -> None:
        """Reset the current value of the calculator to 0."""
        self.value = 0

if __name__ == "__main__":

    # Tests for each method

    c = Calculator()

    c.add(5)
    assert c.value == 5

    c.subtract(2)
    assert c.value == 3

    c.multiply_by(4)
    assert c.value == 12

    c.divide_by(3)
    assert c.value == 4

    c.take_root(2)
    assert c.value == 2

    c.reset_memory()
    assert c.value == 0