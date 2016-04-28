import sys
import re
from sets import Set
from os import listdir
from os.path import isfile, join

def searchVTFamilyFiles(sDirectory):
	files = [f for f in listdir(sDirectory) if isfile(join(sDirectory, f))]
	vtFamilyFiles = []

	for f in files:
		if f.endswith('.family.txt'):
			vtFamilyFiles.append(f)

	vtFamilyFiles.sort()

	for index in range(len(vtFamilyFiles)):
		vtFamilyFiles[index] = join(sDirectory, vtFamilyFiles[index])

	return vtFamilyFiles




def parseVTFamily(sFileName, listFamily):
	fVT = open(sFileName, 'r')
	reVTLine = re.compile(r'([0-9a-f]{32}) ([^\s]+)')

	while True:
		line = fVT.readline()
		if not line:
			break

		match = reVTLine.match(line)
		if match:
			sName = match.group(2)

			if cmp(sName, 'None') == 0:
				continue

			listFamily.append(sName)

	fVT.close()
	return

def parseVTMD5(sFileName, setFamily, listMF):
	fVT = open(sFileName, 'r')
	reVTLine = re.compile(r'([0-9a-f]{32}) ([^\s]+)')

	while True:
		line = fVT.readline()
		if not line:
			break

		match = reVTLine.match(line)
		if match:
			sName = match.group(2)

			if sName in setFamily:
				listMF.append((match.group(1), match.group(2)))

	fVT.close()
	return

if __name__ == '__main__':

	sDirectory = sys.argv[1]
	sTopFamily = sys.argv[2]
	vtFamilyFiles = searchVTFamilyFiles(sDirectory)

	with open(sTopFamily, 'r') as f:
		lines = f.read().splitlines()

	setFamily = Set(lines)

	for f in vtFamilyFiles:
		listMF = []
		parseVTMD5(f, setFamily, listMF)
		foutput = open(f[:-11] + '.top5.family.txt', 'w')
		for MF in listMF:
			foutput.write(MF[0])
			foutput.write(' ')
			foutput.write(MF[1])
			foutput.write('\n')
		foutput.close()
