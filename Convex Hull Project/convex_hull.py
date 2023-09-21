from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



import time

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25

#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

# Class constructor
	def __init__( self):
		super().__init__()
		self.pause = False

# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def showTangent(self, line, color):
		lines = [line]
		self.view.addLines(lines,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		lines = [line]
		self.view.clearLines(lines)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseHull(self,polygon):
		self.view.clearLines(polygon)

	def showText(self,text):
		self.view.displayStatusText(text)

	def find_upper_tangent(self, left_hull, right_hull, leftIndex, rightIndex):
		lenLeft = len(left_hull)
		lenRight = len(right_hull)

		line = QLineF(left_hull[leftIndex], right_hull[rightIndex])
		slope = line.dy() / line.dx()
		done = False
		left = False
		right = False
		
		while not done:
			done = True
			left = False
			right = False
			while not left:
				left = True
				newSlope = (right_hull[rightIndex].y() - left_hull[(leftIndex - 1) % lenLeft].y()) / (right_hull[rightIndex].x() - left_hull[(leftIndex - 1) % lenLeft].x())
				if newSlope < slope:
					left = False
					slope = newSlope
					done = False
					leftIndex = (leftIndex - 1) % lenLeft
			while not right:
				right = True
				newSlope = (right_hull[(rightIndex + 1) % lenRight].y() - left_hull[leftIndex].y()) / (right_hull[(rightIndex + 1) % lenRight].x() - left_hull[leftIndex].x())
				if newSlope > slope:
					right = False
					done = False
					slope = newSlope
					rightIndex = (rightIndex + 1) % lenRight

		return [leftIndex, rightIndex]

	def find_lower_tangent(self, left_hull, right_hull, leftIndex, rightIndex):
		lenLeft = len(left_hull)
		lenRight = len(right_hull)

		line = QLineF(left_hull[leftIndex], right_hull[rightIndex])
		slope = line.dy() / line.dx()
		done = False

		
		while not done:
			done = True
			left = False
			right = False
			while not left:
				left = True
				newSlope = (right_hull[rightIndex].y() - left_hull[(leftIndex + 1) % lenLeft].y()) / (right_hull[rightIndex].x() - left_hull[(leftIndex + 1) % lenLeft].x())
				if newSlope > slope:
					left = False
					slope = newSlope
					done = False
					leftIndex = (leftIndex + 1) % lenLeft
			while not right:
				right = True
				newSlope = (right_hull[(rightIndex - 1) % lenRight].y() - left_hull[leftIndex].y()) / (right_hull[(rightIndex - 1) % lenRight].x() - left_hull[leftIndex].x())
				if newSlope < slope:
					right = False
					done = False
					slope = newSlope
					rightIndex = (rightIndex - 1) % lenRight

		return [leftIndex, rightIndex]
	

	def combine_hulls(self, left_hull, right_hull):
		if(len(left_hull) == 1) and (len(right_hull) == 1):
			return [left_hull[0], right_hull[0]]
		else:
			
			mostRight = max(left_hull, key=lambda left: left.x())
			leftIndex = left_hull.index(mostRight)

			mostLeft = min(right_hull, key=lambda right: right.x())
			rightIndex = right_hull.index(mostLeft)

			upper_tangent = self.find_upper_tangent(left_hull, right_hull, leftIndex, rightIndex)
			lower_tangent = self.find_lower_tangent(left_hull, right_hull, leftIndex, rightIndex)


			combined_hull = []
			lowerLeft = lower_tangent[0]
			lowerRight = lower_tangent[1]
			upperLeft = upper_tangent[0]
			upperRight = upper_tangent[1]

			currentPoint = lowerLeft
			combined_hull.append(left_hull[currentPoint])
			while currentPoint != upperLeft:
				currentPoint = (currentPoint + 1) % len(left_hull)
				combined_hull.append(left_hull[currentPoint])

			currentPoint = upperRight
			combined_hull.append(right_hull[currentPoint])
			while currentPoint != lowerRight:
				currentPoint = (currentPoint + 1) % len(right_hull)
				combined_hull.append(right_hull[currentPoint])
			#polygon = [QLineF(combined_hull[i], combined_hull[(i+1)%len(combined_hull)]) for i in range(len(combined_hull))]
			#self.showHull(polygon, BLUE)
			return combined_hull


	def find_hull(self, points):
		assert( type(points) == list and type(points[0]) == QPointF )
		if(len(points) == 1):
			return points
		else:
			middleIndex = len(points)//2
			firstHalf = points[:middleIndex]
			secondHalf = points[middleIndex:]
			leftHull = self.find_hull(firstHalf)
			rightHull = self.find_hull(secondHalf)
			return self.combine_hulls(leftHull, rightHull)


	
# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull( self, points, pause, view):

		def pointCompare(point):
			return point.x()

		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		points.sort(key=pointCompare)
		t2 = time.time()

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		#polygon = [QLineF(points[i],points[(i+1)%3]) for i in range(3)]
		convex_hull = self.find_hull(points)
		polygon = [QLineF(convex_hull[i], convex_hull[(i+1)%len(convex_hull)]) for i in range(len(convex_hull))]
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))

