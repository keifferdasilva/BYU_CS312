#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


import time
import numpy as np
from TSPClasses import *
import heapq
import itertools


class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution,
		time spent to find solution, number of permutations tried during search, the
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	def greedy( self,time_allowance=60.0 ):
		pass



	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints:
		max queue size, total number of states created, and number of pruned states.</returns>
	'''

	def branchAndBound( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		route = []
		start_time = time.time()
		bssf = self.defaultRandomTour()['soln']
		initialMatrix, lowerBound = self.createDistanceMatrix()
		maxQSize = 1
		totalStates = 1
		prunedStates = 0
		#Queue has key (lowerbound - depth), lowerbound, cost of path so far, the city, the path so far, and the cost matrix
		cityQueue = [(0, lowerBound, 0, [0], initialMatrix)]
		count = 0
		foundTour = False

		while cityQueue and time.time()-start_time < time_allowance:
			key, lowerBound, lastCity, path, distanceMatrix = heapq.heappop(cityQueue)

			if lowerBound >= bssf.cost:
				prunedStates += 1
				continue


			if len(path) == ncities:
				if lowerBound < bssf.cost:
					route = []
					for i in path:
						route.append(cities[i])
					bssf = TSPSolution(route)
					count += 1
					foundTour = True
				continue

			for city in range(ncities):
				if city not in path:
					newPath = path + [city]
					newLowerBound, newDistanceMatrix = self.getLowerBound(lowerBound, distanceMatrix, newPath)
					if newLowerBound >= bssf.cost:
						totalStates += 1
						prunedStates += 1
						continue
					key = newLowerBound / len(newPath)
					heapq.heappush(cityQueue, (key, newLowerBound, city, newPath, newDistanceMatrix))
					totalStates += 1
					if len(cityQueue) > maxQSize:
						maxQSize = len(cityQueue)



		end_time = time.time()
		results['cost'] = bssf.cost
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = maxQSize
		results['total'] = totalStates
		results['pruned'] = prunedStates
		return results


	def createDistanceMatrix(self):
		cities = self._scenario.getCities()
		matrix = np.ones((len(cities), len(cities))) * np.inf
		lowerBound = 0

		for city in range(len(cities)):
			for nextCity in range(len(cities)):
				matrix[city][nextCity] = cities[city].costTo(cities[nextCity])

		for row in range(len(cities)):
			minValue = np.inf
			for col in range(len(cities)):
				if matrix[row][col] < minValue:
					minValue = matrix[row][col]
			for col in range(len(cities)):
				matrix[row][col] = matrix[row][col] - minValue
			lowerBound += minValue

		for col in range(len(cities)):
			minValue = np.inf
			for row in range(len(cities)):
				if matrix[row][col] < minValue:
					minValue = matrix[row][col]
			for row in range(len(cities)):
				matrix[row][col] = matrix[row][col] - minValue
			lowerBound += minValue

		return matrix, lowerBound

	def getLowerBound(self, oldLowerBound, oldMatrix, path):
		distanceMatrix = np.copy(oldMatrix)
		distance = distanceMatrix[path[-2]][path[-1]]
		lowerBound = oldLowerBound + distance
		ncities = distanceMatrix.shape[0]

		for i in range(ncities):
			distanceMatrix[path[-2]][i] = np.inf
			distanceMatrix[i][path[-1]] = np.inf

		distanceMatrix[path[-1]][path[-2]] = np.inf

		for row in range(ncities) :
			if row == path[-2]:
				continue
			minValue = np.inf
			for col in range(ncities):
				if col == path[-1]:
					continue
				if distanceMatrix[row][col] < minValue:
					minValue = distanceMatrix[row][col]
			if minValue != np.inf:
				for col in range(ncities):
					distanceMatrix[row][col] = distanceMatrix[row][col] - minValue if distanceMatrix[row][col] > 0 else 0
				lowerBound += minValue

		for col in range(ncities):
			if col == path[-1]:
				continue
			minValue = np.inf
			for row in range(ncities):
				if row == path[-2]:
					continue
				if distanceMatrix[row][col] < minValue:
					minValue = distanceMatrix[row][col]
			if minValue != np.inf:
				for row in range(ncities):
					distanceMatrix[row][col] = distanceMatrix[row][col] - minValue if distanceMatrix[row][col] > 0 else 0
				lowerBound += minValue

		return lowerBound, distanceMatrix


	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found during search, the
		best solution found.  You may use the other three field however you like.
		algorithm</returns>
	'''

	def fancy( self,time_allowance=60.0 ):
		pass
