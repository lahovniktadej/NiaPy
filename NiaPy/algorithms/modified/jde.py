# encoding=utf8
# pylint: disable=mixed-indentation, multiple-statements, logging-not-lazy, attribute-defined-outside-init, line-too-long, arguments-differ
import logging
from numpy import argmin
from NiaPy.algorithms.algorithm import Individual
from NiaPy.algorithms.basic.de import DifferentialEvolutionAlgorithm

logging.basicConfig()
logger = logging.getLogger('NiaPy.algorithms.modified')
logger.setLevel('INFO')

__all__ = ['SelfAdaptiveDifferentialEvolutionAlgorithm']

class SolutionjDE(Individual):
	def __init__(self, **kwargs):
		Individual.__init__(self, **kwargs)
		self.F, self.CR = kwargs.get('F', 2), kwargs.get('CR', 0.5)

class SelfAdaptiveDifferentialEvolutionAlgorithm(DifferentialEvolutionAlgorithm):
	r"""Implementation of Self-adaptive differential evolution algorithm.

	**Algorithm:** Self-adaptive differential evolution algorithm

	**Date:** 2018

	**Author:** Uros Mlakar and Klemen Berkvoič

	**License:** MIT

	**Reference paper:**
	Brest, J., Greiner, S., Boskovic, B., Mernik, M., Zumer, V.
	Self-adapting control parameters in differential evolution:
	A comparative study on numerical benchmark problems.
	IEEE transactions on evolutionary computation, 10(6), 646-657, 2006.
	"""
	def __init__(self, **kwargs): DifferentialEvolutionAlgorithm.__init__(self, name='SelfAdaptiveDifferentialEvolutionAlgorithm', sName='jDE', **kwargs)

	def setParameters(self, F_l=0.0, F_u=2.0, Tao1=0.4, Tao2=0.6, **ukwargs):
		r"""Set the parameters of an algorithm.

		Arguments:
		F_l {decimal} -- scaling factor lower limit
		F_u {decimal} -- scaling factor upper limit
		Tao1 {decimal} -- change rate for F parameter update
		Tao2 {decimal} -- change rate for CR parameter update
		"""
		DifferentialEvolutionAlgorithm.setParameters(self, **ukwargs)
		self.F_l, self.F_u, self.Tao1, self.Tao2 = F_l, F_u, Tao1, Tao2
		if ukwargs: logger.info('Unused arguments: %s' % (ukwargs))

	def AdaptiveGen(self, x):
		f = self.F_l + self.rand() * (self.F_u - self.F_l) if self.rand() < self.Tao1 else x.F
		cr = self.rand() if self.rand() < self.Tao2 else x.CR
		return SolutionjDE(x=x.x, F=f, CR=cr)

	def runTask(self, task):
		pop = [SolutionjDE(task=task, F=self.F, CR=self.CR) for _i in range(self.Np)]
		x_b = pop[argmin([x.f for x in pop])]
		while not task.stopCond():
			npop = [self.AdaptiveGen(pop[i]) for i in range(self.Np)]
			npop = [SolutionjDE(x=self.CrossMutt(npop, i, x_b, self.F, self.CR, self.Rand), F=npop[i].F, CR=npop[i].CR, e=False) for i in range(self.Np)]
			pop = [self.evalPopulation(npop[i], pop[i], task) for i in range(self.Np)]
			ix_b = argmin([x.f for x in pop])
			if x_b.f > pop[ix_b].f: x_b = pop[ix_b]
		return x_b.x, x_b.f

# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
