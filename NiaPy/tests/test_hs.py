# encoding=utf8
# pylint: disable=mixed-indentation, multiple-statements
from unittest import TestCase
from NiaPy.benchmarks.griewank import Griewank
from NiaPy.algorithms.basic import BareBonesFireworksAlgorithm

class MyBenchmark:
	def __init__(self):
		self.Lower = -5.12
		self.Upper = 5.12

	@classmethod
	def function(cls):
		def evaluate(D, sol):
			val = 0.0
			for i in range(D): val = val + sol[i] * sol[i]
			return val
		return evaluate

class BBFWATestCase(TestCase):
	def setUp(self):
		self.D = 40
		self.bbfa_custom = BareBonesFireworksAlgorithm(D=self.D, nFES=1000, n=10, C_a=2, C_r=0.5, benchmark=MyBenchmark())
		self.bbfa_griewank = BareBonesFireworksAlgorithm(D=self.D, nFES=1000, n=10, C_a=5, C_r=0.5, benchmark=Griewank())

	def test_custom_works_fine(self):
		fun = MyBenchmark().function()
		x = self.bbfa_custom.run()
		self.assertTrue(x)
		self.assertAlmostEqual(fun(self.D, x[0]), x[1], delta=1e2)

	def test_griewank_works_fine(self):
		fun = Griewank().function()
		x = self.bbfa_griewank.run()
		self.assertTrue(x)
		self.assertAlmostEqual(fun(self.D, x[0]), x[1], delta=1e2)

# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
