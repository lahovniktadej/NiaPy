# encoding=utf8
# pylint: disable=anomalous-backslash-in-string
"""Implementation of Csendes function.

Date: 2018

Author: Lucija Brezočnik

License: MIT

Function: Csendes function

Input domain:
    The function can be defined on any input domain but it is usually
    evaluated on the hypercube x_i ∈ [-1, 1], for all i = 1, 2,..., D.

Global minimum:
    f(x*) = 0, at x* = (0,...,0)

LaTeX formats:
    Inline: $f(\mathbf{x}) = \sum_{i=1}^D x_i^6\left( 2 + sin \frac{1}{x_i}\right)$
    Equation:  \begin{equation} f(\mathbf{x}) =
               \sum_{i=1}^D x_i^6\left( 2 + sin \frac{1}{x_i}\right) \end{equation}
    Domain: $-1 \leq x_i \leq 1$

Reference paper:
    Jamil, M., and Yang, X. S. (2013).
    A literature survey of benchmark functions for global optimisation problems.
    International Journal of Mathematical Modelling and Numerical Optimisation,
    4(2), 150-194.
"""

import math

__all__ = ['Csendes']


class Csendes(object):

    def __init__(self, Lower=-1.0, Upper=1.0):
        self.Lower = Lower
        self.Upper = Upper

    @classmethod
    def function(cls):
        def evaluate(D, sol):

            val = 0.0

            for i in range(D):
                val += math.pow(sol[i], 6) * (2.0 + math.sin(1.0 / sol[i]))

            return val

        return evaluate
