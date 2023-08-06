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

from gensarpy.convergence_tests import check_convergence

series1 = "1/n**2"
result1 = check_convergence(series1)
print(f"The series {series1} is {result1}.")

series2 = "1/2**n"
result2 = check_convergence(series2)
print(f"The series {series2} is {result2}.")

series3 = "(-1)**n/n"
result3 = check_convergence(series3)
print(f"The series {series3} is {result3}.")
 
This will output:

The series 1/n**2 is convergent.
The series 1/2**n is convergent.
The series (-1)**n/n is divergent.


The check_convergence function takes two arguments: the series (as a list) and the test type. The available test types are p, ratio, integral, and alternating.

***************************



Contributing
------------
Contributions to Gensarpy are welcome! To contribute, please fork the repository, create a branch for your changes, and submit a pull request. Before submitting a pull request, please make sure that your code passes the existing tests and that any new functionality is covered by new tests.

***************************



License
-------
Gensarpy is released under the MIT License.
