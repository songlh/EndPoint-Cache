

class Node:
	def __init__(self, k, x):
		self.key = k
		self.val = x
		self.prev = None
		self.next = None

class DoubleLinkedList:
	def __init__(self):
		self.tail = None
		self.head = None

	def isEmpty(self):
		return not self.tail

	def remove(self, node):
		if self.head == self.tail:
			self.head = None
			self.tail = None
			return 

		if node == self.head:
			node.next.prev = None
			self.head = node.next
			return

		if node == self.tail:
			node.prev.next = None
			self.tail = node.prev
			return

		node.prev.next = node.next
		node.next.prev = node.prev

	def removeLast(self):
		self.remove(self.tail)

	def addFirst(self, node):
		if not self.head:
			self.head = self.tail = node
			node.prev = node.next =None
			return

		node.next = self.head
		self.head.prev = node
		self.head = node
		node.prev = None

	