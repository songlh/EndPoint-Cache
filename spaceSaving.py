import sys

class Counter:
	IDCounterMapping = {}
	def __init__(self, ID, xi, bucket=None):
		self.sID = ID
		self.Xi = xi
		self.bucket = bucket
		self.prev = None
		self.next = None
		Counter.IDCounterMapping[ID] = self

	def detach(self):
		if self.bucket.head == self:
			self.bucket.head = self.next

		if self.prev != self:
			self.prev.next = self.next
			self.next.prev = self.prev
		else:
			self.bucket.head = None

		self.prev = None
		self.next = None
		self.bucket = None


	def attach(self, bucket):
		if bucket.head == None:
			bucket.head = self
			self.prev = self
			self.next = self
			self.bucket = bucket
			return

		bucket.head.prev.next = self
		self.prev = bucket.head.prev
		self.next = bucket.head
		bucket.head.prev = self

		self.bucket = bucket

	def changeID(self, ID):
		del Counter.IDCounterMapping[self.sID]
		self.sID = ID
		Counter.IDCounterMapping[ID] = self


	@staticmethod
	def isIDMonitored(ID):
		return ID in Counter.IDCounterMapping

	@staticmethod
	def getCounter(ID):
		if ID in Counter.IDCounterMapping:
			return Counter.IDCounterMapping[ID]

		return None

	@staticmethod
	def getMonitoredNum():
		return len(Counter.IDCounterMapping)



class Bucket:
	ValueBucketMapping = {}
	def __init__(self, value):
		self.value = value
		self.head = None
		self.prev = None
		self.next = None
		Bucket.ValueBucketMapping[value] = self





class StreamSummary:
	def __init__(self, m):
		self.bucketHead = None
		self.maxCounter = m



def IncrementCounter(summary, count):
	bucket = count.bucket
	bucketplus = bucket.next
	count.detach()
	countValue = bucket.value
	countValue += 1


	if bucketplus != None and bucketplus.value == countValue:
		count.attach(bucketplus)
	else:
		bucketNew = Bucket(countValue)
		count.attach(bucketNew)
		if bucketplus == None:
			bucket.next = bucketNew
			bucketNew.prev = bucket
		else:
			bucketplus.prev = bucketNew
			bucketNew.next = bucketplus
			bucketNew.prev= bucket
			bucket.next = bucketNew

	if bucket.head == None:
		if summary.bucketHead == bucket:
			summary.bucketHead = bucket.next
		else:
			bucket.prev.next = bucket.next
			if bucket.next != None:
				bucket.next.prev = bucket.prev

		del Bucket.ValueBucketMapping[bucket.value]

def AddCounter(summary, count):
	if 1 in Bucket.ValueBucketMapping:
		bucket = Bucket.ValueBucketMapping[1]
	else:
		bucket = Bucket(1)
		if summary.bucketHead == None:
			summary.bucketHead = bucket
		else:
			summary.bucketHead.prev = bucket
			bucket.next = summary.bucketHead
			summary.bucketHead = bucket

	count.attach(bucket)


def SpaceSaving(summary, ID):
	if Counter.isIDMonitored(ID):
		count = Counter.getCounter(ID)
		IncrementCounter(summary, count)
	else:
		if Counter.getMonitoredNum() < summary.maxCounter:
			count = Counter(ID, 0)
			AddCounter(summary, count)
		else:
			minhits = summary.bucketHead.value
			count = summary.bucketHead.head
			count.changeID(ID)

			IncrementCounter(summary, count)
			count.Xi = minhits

def printStreamSummary(summary):
	bucketHead = summary.bucketHead

	while bucketHead != None:
		countHead = bucketHead.head
		currentCount = countHead
		print currentCount.sID, bucketHead.value, currentCount.Xi 

		currentCount = currentCount.next
		while currentCount != countHead:
			print currentCount.sID, bucketHead.value, currentCount.Xi
			currentCount = currentCount.next

		bucketHead = bucketHead.next



if __name__ == '__main__':
	#sInput = 'ABBACABBDDBEC'
	sInput = "aaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbccccccccccccccccccccccccccceeeeeeeefffgggggggggghhhhhhhh"
	index = 0
	summary = StreamSummary(3)

	while index < len(sInput):
		SpaceSaving(summary, sInput[index])
		index += 1

		#if index == 13:
		#	break
		
	#printStreamSummary(summary)