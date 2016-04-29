import os
import sys
import numpy as np
from os.path import isfile, join

def locateFPFile(directoryList, md5):
	sFPFileName = None
	for directory in directoryList:
		
		if os.path.exists(join(directory, md5 + '.bb')):
			sFPFileName = join(directory, md5 + '.bb')
			break

	return sFPFileName

def loadFPtoNPMatrix(sFileName):
	fpMatrix = np.zeros((1, 240007))
	fFP = open(sFileName, 'r')

	sFirstLine = fFP.readline()
	sSecondLine = fFP.readline()

	iNum = int(sFirstLine)

	while True:
		line = fFP.readline()
		if not line:
			break

		numList = line.split()
		fpMatrix[0, int(numList[0])] = 1

	fFP.close()
	return fpMatrix

def batchLoadFPtoNPMatrix(listFileName):
	fpMatrix = np.zeros((len(listFileName), 240007))
	
	for index in range(len(listFileName)):
		#print listFileName[index]
		fpVector = loadFPtoNPMatrix(listFileName[index])
		fpMatrix[index:] = fpVector
				

	return fpMatrix

def batchLoadMD5List(directoryList, md5List):
	listFileName = []
	md5NewList = []
	for md5 in md5List:
		sFileName = locateFPFile(directoryList, md5)
		if sFileName != None:
			listFileName.append(sFileName)
			md5NewList.append(md5)
			

	#print len(listFileName)	
	return batchLoadFPtoNPMatrix(listFileName), md5NewList
