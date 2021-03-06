import sys
import LRU
import numpy as np
import parser.vtFamily
import parser.FP


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
		self.cache = LRU.DoubleLinkedList()
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
		#print fpVector.shape
		assert fpVector.shape[0] == 1
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
			node = LRU.Node(key, md5)
			self.KMap[key] = node
			self.cache.addFirst(node)
			self.size += 1

		#print self.hits, self.miss, self.hits * 1.0 / (self.hits + self.miss)

if __name__ == '__main__':
	sMD5ListDirectory = sys.argv[1]
	sFPDirectoryFile = sys.argv[2]
	numSize = int(sys.argv[3])
	cache = LRUPFCache(numSize)	

	top5List = parser.vtFamily.searchTop5VTFamilyFiles(sMD5ListDirectory) 

	assert len(top5List) > 1

	with open(sFPDirectoryFile, 'r') as f:
		directoryList = f.readlines()

	directoryList = [directory[:-1] for directory in directoryList]
	
	
	md5List = []
	parser.vtFamily.parseVTTotalMD5(top5List[0], md5List)
	fpMatrix, md5NewList = parser.FP.batchLoadMD5List(directoryList, md5List)

	#print fpMatrix.shape, len(md5NewList)
	for i in range(fpMatrix.shape[0]):
		cache.check(fpMatrix[[i],], md5NewList[i])
		
		if (i + 1) % 50 == 0:
			print 'Hit:', cache.hits, 'Miss:', cache.miss, 'Hit Rate:', cache.hits * 1.0 / (cache.hits + cache.miss)
		

	index = 1
	while index < len(top5List):
		md5List = []
		parser.vtFamily.parseVTTotalMD5(top5List[index], md5List)
		fpMatrix, md5NewList = parser.FP.batchLoadMD5List(directoryList, md5List)
		cache.batchcheck(fpMatrix)

		print 'Batch Hit:', cache.batchhits
		print 'Batch Miss', cache.batchmiss
		print 'Batch Hit Rate:', cache.batchhits * 1.0 / (cache.batchhits + cache.batchmiss)
	
		for i in range(fpMatrix.shape[0]):
			cache.check(fpMatrix[[i],], md5NewList[i])
			if (i + 1) % 50 == 0:
                        	print 'Hit:', cache.hits, 'Miss:', cache.miss, 'Hit Rate:', cache.hits * 1.0 / (cache.hits + cache.miss)

		#index += 1
		#break

	#print 'Batch Hit:', cache.batchhits
	#print 'Batch Miss', cache.batchmiss
	#print 'Batch Hit Rate:', cache.batchhits * 1.0 / (cache.batchhits + cache.batchmiss)

	#for top5 in top5List:
	#	md5List = []
	#	parser.vtFamily.parseVTTotalMD5(top5, md5List)
	print 'Hit:', cache.hits, 'Miss:', cache.miss, 'Hit Rate:', cache.hits * 1.0 / (cache.hits + cache.miss)

