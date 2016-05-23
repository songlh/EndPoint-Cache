import parser.vtFamily
import spaceSaving
import sys

def loadFamilyList(sDataFile):
	with open(sDataFile, 'r') as f:
		lines = f.read().splitlines()

	vtFamilyFiles = []
	for line in lines:
		vtFamilyFiles = vtFamilyFiles + parser.vtFamily.searchVTFamilyFiles(line)

	listFamilyAll = []
	for f in vtFamilyFiles:
		parser.vtFamily.parseVTFamily(f, listFamilyAll)

	listFamily = []
	for familyName in listFamilyAll:
		if familyName.startswith('Microsoft$'):
			listFamily.append(familyName)

	return listFamily


def statFamilyList(listFamily):

	total = len(listFamily)
	countDict = {}
	for family in listFamily:
		if family not in countDict:
			countDict[family] = 0

		countDict[family] += 1

	print len(countDict)

	rankResult = sorted(countDict.items(), key = lambda x:x[1], reverse=True)

	i = 0
	while i < 20 and i < len(rankResult):
		print rankResult[i][0], rankResult[i][1], rankResult[i][1] * 1.0 / total
		i += 1



if __name__=='__main__':
	sDataFile = sys.argv[1]
	listFamily = loadFamilyList(sDataFile)

	summary = spaceSaving.StreamSummary(100)

	for family in listFamily:
		spaceSaving.SpaceSaving(summary, family)

	spaceSaving.printStreamSummary(summary)