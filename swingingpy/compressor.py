"""Contains the compression algorithm"""
import math

class CPoint:
    """A simple Point object used by the SwingingDoor.
    """
    _x = None
    _y = None

    def __init__(self, x: float, y: float):
        """Create a new virtual point used in the Compressor.

        Args:
            x (float): The x axis.
            y (float): The y axis.
        """
        self._x = x
        self._y = y

    def get_x(self):
        """Get the x axis.

        Returns:
            float: X axis.
        """
        return self._x

    def get_y(self):
        """Get the y axis.

        Returns:
            float: Y axis.
        """
        return self._y

class SwingingDoor:
    """Compress data using the SwingingDoor algorithm.

    Returns:
        [SwingingDoor]: A new SwingingDoor object.
    """

    __comp_dev = None
    __comp_max = None
    __slope_high = None
    __slope_low = None
    __point_count = 0
    __point_stored = 0

    snap_point = None
    original = None

    def __init__(self, comp_dev: float, comp_max: float = -1, original: CPoint = None, snapshot: CPoint = None):
        """Create a new SwingingDoor object.

        Args:
            comp_dev (float): The compression angle.
            comp_max (float, optional): The maximum time after forcing the point storage. Defaults to -1.
            original (CPoint, optional): The original point. Defaults to None.
            snapshot (CPoint, optional): The snapshot point. Defaults to None.
        """
        self.__comp_dev = comp_dev
        self.__comp_max = comp_max
        self.original = original

        self.__slope_low = -math.inf
        self.__slope_high = math.inf

        if snapshot is not None:
            self.snap_point = snapshot
            self.__slope_high = min(
                self.__slope_high,
                (self.snap_point.y + self.__comp_dev - self.original.y) / (self.snap_point.x - self.original.x))
            self.__slope_low = max(
                self.__slope_low,
                (self.snap_point.y - self.__comp_dev - self.original.y) / (self.snap_point.x - self.original.x))


    def calculate_window(self, point: CPoint):
        """Calculate a new window.

        Args:
            point (CPoint): The point to calculate the new window.
        """

        # reset the angle
        self.__slope_low = -math.inf
        self.__slope_high = math.inf

        # set the new original point
        if self.snap_point is not None:
            self.original = self.snap_point
        self.snap_point = point


    def check(self, point: CPoint):
        """Check if a point need to be stored.

        Args:
            point (CPoint): The Point to test.

        Returns:
            CPoint: The point which need to be stored.
        """
        store = None
        self.__point_count += 1

        # if first point
        if self.original is None:
            self.original = point
            return point

        # calculate the slope
        slope = (point.get_y() - self.original.get_y()) / (point.get_x() - self.original.get_x())
        time_diff = point.get_x() - self.original.get_x()

        # point is outside of the angle or com_max is exeeded
        if slope < self.__slope_low or slope > self.__slope_high:
            store = self.snap_point
            self.calculate_window(point)
            self.__point_stored += 1

            return store

        # point is outside the time limit
        if self.__comp_max != -1 and time_diff >= self.__comp_max:
            store = point
            self.calculate_window(point)
            self.__point_stored += 1

        # reduce the angle
        self.__slope_high = min(
            self.__slope_high,
            (point.get_y() + self.__comp_dev - self.original.get_y()) / (point.get_x() - self.original.get_x()))
        self.__slope_low = max(
            self.__slope_low,
            (point.get_y() - self.__comp_dev - self.original.get_y()) / (point.get_x() - self.original.get_x()))


        # set the snapshot point
        self.snap_point = point

        return store

    def get_compression_ratio(self):
        """Get the current compression ratio.

        Returns:
            float: The ratio level in percent.
        """

        if self.__point_stored == 0:
            return 100

        return 100 - 100 / (self.__point_count / self.__point_stored)
