import LRU
import numpy as np


def computeFPScoreMatrix(fpMatrix1, fpMatrix2):
	scoreMatrix = fpMatrix1.dot(fpMatrix2)
	matrixSum = np.sum(fpMatrix2, axis = 0)

	for i in range(0, fpMatrix2.shape[1]):
		if matrixSum[i] == 0:
			for j in range(0, fpMatrix1.shape[0]):
				scoreMatrix[j, i] = 0

		else:
			for j in range(0, fpMatrix1.shape[0]):
				scoreMatrix[j, i] = scoreMatrix[j, i] * 1.0 / matrixSum[i]

	return scoreMatrix


class LRUPFCache:
	def __init__(self, capacity):
		self.capacity = capacity
		self.size = 0
		self.fpMatrix = np.zeros((240007, capacity))
		self.KMap = {}
		self.cache = DoubleLinkedList()
		self.hits = 0
		self.miss = 0
		self.batchhits = 0
		self.batchmiss = 0

	def batchcheck(self, fpVector):
		scoreMatrix = computeFPScoreMatrix(fpVector, self.fpMatrix)
		matchMatrix = scoreMatrix >= 0.9

		for i in range(matchMatrix.shape[0]):
			index = 0
			while index < self.size:
				if matchMatrix[i, index]:
					break
				index += 1

			if index < self.size:
				self.batchhits += 1
			else:
				self.batchmiss += 1

	def check(self, fpVector, md5):
		assert fp.shape[0] == 1
		scoreMatrix = computeFPScoreMatrix(fpVector, self.fpMatrix)
		matchMatrix = scoreMatrix >= 0.9

		i = 0
		while i < self.size:
			if matchMatrix[0, i]:
				break
			i += 1

		if i < self.size:
			self.hits += 1
			self.cache.remove(self.KMap[i])
			self.cache.addFirst(self.KMap[i])

		else:
			self.miss += 1
			if i < self.capacity:
				key = i
			else:
				key = self.cache.tail.key
				self.cache.removeLast()
				self.size -= 1

			self.fpMatrix[:, key] = np.transpose(fpVector[0])
			node = Node(key, md5)
			self.KMap[key] = node
			self.cache.addFirst(node)
			self.size += 1

		print self.hits, self.miss, self.hits * 1.0 / (self.hits + self.miss)

if __name__ == '__main__':
	a = np.matrix([[1,2], [3,4]])
	print a[0].shape