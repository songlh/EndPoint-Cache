import sys
import re
import FP

def clusterParser(sFileName):
	fCluster = open(sFileName, 'r')
	reCluster = re.compile(r'Cluster ([0-9]+) has ([0-9]+) apps: ([^\n]+)')
	
	clusterList = []

	while True:
		line = fCluster.readline()
		if not line:
			break
		
		match = reCluster.match(line)
		if match:
			num = int(match.group(2))
			appIndex = [int(n) for n in match.group(3).split()]
			clusterList.append(appIndex)

	fCluster.close()
	return clusterList


if __name__=='__main__':
	sClusterFile = sys.argv[1]
	sFPListFile = sys.argv[2]

	clusterList = clusterParser(sClusterFile)
	with open(sFPListFile, 'r' ) as f:
		FPList = f.readlines()

	FPList = [fp[:-1] for fp in FPList]

	for i in range(len(clusterList)):
		cluster = clusterList[i]

		if len(cluster) == 1:
			continue

		
		setFP = FP.loadFPtoSet(FPList[cluster[0]])
		index = 1

		print i, len(cluster), len(setFP),

		while index < len(cluster):
			setFP = setFP.intersection(FP.loadFPtoSet(FPList[cluster[index]]))
			index += 1	

		print len(setFP)
	
	
