import sys
import unittest

sys.path.append('/Users/gencersarpmert/mypackage/src/gensarpy/convergence_tests.py')

from convergence_tests.convergence_tests import check_convergence, p_series_test, ratio_test, integral_test



class TestConvergenceTests(unittest.TestCase):
    def test_check_convergence_nth_term(self):
        self.assertEqual(check_convergence('1/n'), 'Convergent')

    def test_check_convergence_integral(self):
        self.assertEqual(check_convergence('1/x**2'), 'Convergent')

    def test_check_convergence_ratio(self):
        self.assertEqual(check_convergence('1/n**2'), 'Convergent')

    def test_check_convergence_alternating(self):
        self.assertEqual(check_convergence('(-1)**n/n'), 'Convergent')

    def test_check_convergence_pseries(self):
        self.assertEqual(check_convergence('1/x**3'), 'Convergent')

if __name__ == '__main__':
    unittest.main()

# series1 = 'x**-5'
# result1 = check_convergence(series1)
# print(f"The series {series1} is {result1}.")
# #divergent

# series2 = "1/x**2"
# result2 = check_convergence(series2)
# print(f"The series {series2} is {result2}.")
# # convergent

# series3 = "1/(n*log(n))"
# result3 = check_convergence(series3)
# print(f"The series {series3} is {result3}.")
# #divergent

# series4 = "x"
# result4 = check_convergence(series4)
# print(f"The series {series4} is {result4}.")
# # divergent

# series5 = "(3**x)/(2**x-1)"
# result5 = check_convergence(series5)
# print(f"The series {series5} is {result5}.")
# # divergent

# series6 = "x**(1-pi)"
# result6 = check_convergence(series6)
# print(f"The series {series6} is {result6}.")
# # convergent


