Calculator Package
==================

The `calculator` package provides a `Calculator` class that can be used to perform basic arithmetic operations.

Installation
------------

To install the `calculator` package, run:

pip install calculatorAG

Usage
-----

To use the `Calculator` class, first import it:

from calculator.calculator import Calculator


Then create a new Calculator object:

calculator = Calculator()


You can then use the following methods to perform arithmetic operations:

add(value: float) -> float: Adds a value to the calculator's memory and returns the updated value.

subtract(value: float) -> float: Subtracts a value from the calculator's memory and returns the updated value.

multiply(value: float) -> float: Multiplies the calculator's memory by a value and returns the updated value.

divide(value: float) -> float: Divides the calculator's memory by a value and returns the updated value.

root(value: float) -> float: Calculates the nth root of the calculator's memory, where n is the value, and returns the updated value.

reset() -> None: Resets the calculator's memory to 0.


For example:

calculator = Calculator()

result = calculator.add(10)  # 10
result = calculator.subtract(5)  # 5
result = calculator.multiply(2)  # 10
result = calculator.divide(5)  # 2
result = calculator.root(2)  # 1.4142135623730951
calculator.reset()  # memory is now 0


Testing

The calculator package includes a test suite that can be run using unittest. To run the tests, navigate to the package directory and run:

python -m unittest discover

This will discover and run all the tests in the tests directory.


License

The calculator package is released under the MIT License.
See LICENSE.txt for more information.
Of course, you can modify the contents of the README file to suit your specific needs. Just make sure to include information about how to install and use the package, and any other relevant details that you think users might need to know.


