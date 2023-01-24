import math

from utils import rnd


class Num:
	"""
	Summarizes a stream of numbers.
	"""
	def __init__(self, at, txt):
		self.at = at or 0
		self.txt = txt or ""

		self.n = 0
		self.mu = 0
		self.m2 = 0

		self.lo = math.inf
		self.hi = -math.inf

	def add(self, n: float) -> None:
		"""
		Adds n and updates lo, hi and stuff needed for standard deviation.

		:param n: Number to add
		:return: None
		"""
		if n != "?":
			self.n += 1

			d = n - self.mu

			self.mu += (d / self.n)
			self.m2 += d * (n - self.mu)

			self.lo = min(n, self.lo)
			self.hi = max(n, self.hi)

	def mid(self) -> float:
		"""
		Returns mean of the numbers added to the stream.

		:return: Mean of the numbers
		"""
		return self.mu

	def div(self) -> float:
		"""
		Returns standard deviation of the numbers using Welford's algorithm.

		:return: Standard deviation of the numbers
		"""
		return 0 if (self.m2 < 0 or self.n < 2) else math.pow((self.m2 / (self.n - 1)), 0.5)

	@staticmethod
	def rnd(x, n):
		"""
		Returns a rounded number

		:param x: Number to round
		:param n: Number of decimal places to round
		:return: Rounded number
		"""
		return x if x == "?" else rnd(x, n)



