Gensarpy
--------

Gensarpy is a Python package that includes different tests to distinguish series as convergent or divergent. This package provides an easy-to-use interface to check the convergence of series using various tests.

***************************



Installation
------------

You can install Gensarpy using pip. To install the latest release, run:

pip install gensarpy

***************************



Usage
-----

To use Gensarpy, import the functions you need from the package and call them with the appropriate arguments. Here's an example:

from gensarpy.convergence_tests import check_convergence,isdivergent,integral_test 

series1 = "1/n**2"
result1 = check_convergence(series1)
print(f"The series {series1} is {result1}.")

series2 = "1/2**n"
result2 = isdivergent(series2)
print(result2)

series3 = "(-1)**n/n"
result3 = integral_test(series3)
print(f"The series {series3} is {result3}.")
 
This will output:

The series 1/n**2 is convergent.
False
The series (-1)**n/n is divergent.

Here is a list of functions in the gensarpy library:
- integral_test
- ratio_test
- nth_term_test
- check_convergense
- isconvergent
- isdivergent

They all take as a string as input. You should use 'x' as your variable.


***************************



Contributing
------------
Contributions to Gensarpy are welcome! To contribute, please fork the repository, create a branch for your changes, and submit a pull request. Before submitting a pull request, please make sure that your code passes the existing tests and that any new functionality is covered by new tests.

***************************



License
-------
Gensarpy is released under the MIT License.
