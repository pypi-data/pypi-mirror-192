## Calculator
This is a simple Python calculator that supports addition, subtraction, multiplication, and division, as well as taking roots.

## Installation
You can install calculator using pip. First, open a terminal window and run the following command:
```
pip install calculator_2023_02_15
```

## Usage
To use the calculator, first import the Calculator class and create an instance of it:
```python
from calculator_2023_02_15.calculator import Calculator

calculator = Calculator()
```

You can then use the following methods to perform calculations:
add(x): Add x to the current value in the calculator.
subtract(x): Subtract x from the current value in the calculator.
multiply_by(x): Multiply the current value in the calculator by x.
divide_by(x): Divide the current value in the calculator by x.
take_root(x): Take the xth root of the current value in the calculator.
reset_memory(): Reset the value in the calculator to 0.

Here's an example usage:
```python
calculator = Calculator()

calculator.add(5)
print(calculator.value)    # Output: 5

calculator.multiply_by(3)
print(calculator.value)    # Output: 15

calculator.divide_by(2)
print(calculator.value)    # Output: 7.5

calculator.take_root(3)
print(calculator.value)    # Output: 1.9365

calculator.reset_memory()
print(calculator.value)    # Output: 0
```

## Requirements
The package does not have any external dependencies.

## License
[MIT](https://choosealicense.com/licenses/mit/)