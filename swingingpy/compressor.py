
import math

class CPoint:
	"""A simple Point object used by the SwingingDoor
	"""
	x = None
	y = None

	def __init__(self, x:float, y:float):
		"""Create a new virtual point used in the Compressor

		:param x: The x axis
		:type x: float
		:param y: The y axis
		:type y: float
		"""
		self.x = x
		self.y = y

class SwingingDoor:
	"""Compress data using the SwingingDoor algorithm

	:return: A new SwingingDoor object
	:rtype: SwingingDoor
	"""

	__comp_dev = None
	__comp_max = None
	__slope_high = None
	__slope_low  = None
	__point_count = 0
	__point_stored = 0

	snap_point = None
	original = None

	def __init__(self, comp_dev:float, comp_max:float=-1, original:CPoint=None, snapshot:CPoint=None):
		"""Create a new SwingingDoor object

		:param comp: The compression angle
		:type comp: float
		:param original: The original point
		:type original: CPoint
		:param snapshot: The snapshot point, defaults to None
		:type snapshot: CPoint, optional
		:param comp_max: The max time after force storing point, defaults to -1
		:type comp_max: float, optional
		"""
		self.__comp_dev = comp_dev
		self.__comp_max = comp_max
		self.original = original

		self.__slope_low  = -math.inf
		self.__slope_high = math.inf

		if snapshot is not None:
			self.snap_point = snapshot #maybe useless ?
			self.__slope_high = min(self.__slope_high, (self.snap_point.y + self.__comp_dev - self.original.y) / (self.snap_point.x - self.original.x))
			self.__slope_low = max(self.__slope_low, (self.snap_point.y - self.__comp_dev - self.original.y) / (self.snap_point.x - self.original.x))


	def calculate_window(self, point:CPoint):
		"""Calculate a new window

		:param point: [description]
		:type point: CPoint
		"""

		# reset the angle
		self.__slope_low  = -math.inf
		self.__slope_high = math.inf

		# set the new original point
		if self.snap_point is not None:
			self.original = self.snap_point
		self.snap_point = point

		self.__point_count += 1


	def check(self, point: CPoint):
		"""Check if a point need to be stored

		:param point: The CPoint to test
		:type point: CPoint
		:return: A list of points to store
		:rtype: CPoint[]
		"""
		store = None

		# if first point
		if self.original is None:
			self.original = point
			# self.calculate_window(point)
			return point

		# calculate the slope
		slope = (point.y - self.original.y) / (point.x - self.original.x)
		time_diff =  point.x - self.original.x

		# point is outside of the angle or com_max is exeeded
		if slope < self.__slope_low or slope > self.__slope_high:
			# print(f"{slope} < {self.__slope_low} or {slope} > {self.__slope_high}")
			store = self.snap_point
			self.calculate_window(point)
			self.__point_stored += 1

			return store

		elif time_diff >= self.__comp_max:
			# print(f"{point.x} - {self.original.x} = {time_diff}")
			# print(f" {time_diff} >= {self.__comp_max}")
			store = point
			self.calculate_window(point)
			self.__point_stored += 1

		# reduce the angle
		self.__slope_high = min(self.__slope_high, (point.y + self.__comp_dev - self.original.y) / (point.x - self.original.x))
		self.__slope_low = max(self.__slope_low, (point.y - self.__comp_dev - self.original.y) / (point.x - self.original.x))


		# set the snapshot point
		self.snap_point = point
		self.__point_count += 1

		return store

	def get_compression_ratio(self):
		"""Get the current compression ratio

		:return: The ratio level in percent
		:rtype: float
		"""

		if self.__point_stored == 0:
			return 100
		return 100 - 100 / (self.__point_count / self.__point_stored)
