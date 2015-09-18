import Queue

class newQueue(Queue.Queue):
	def __init__(self):
		Queue.Queue.__init__(self)
	def put(self, arg):
		try:
			arg+=1
			Queue.Queue.put(self,arg-1)
		except TypeError:
			print "Can only add integers to the queue."
	def pop(self):
		return self.get()

class Stack():
	"""stack using	a	list	to	store	the	stack	data"""
	def __init__(self):
		self.data = []

	def push(self, number):
		self.data.append(number)
		return

	def pop(self):
		return self.data.pop()

	def checkSize(self):
		return len(self.data)

class BinaryTree():
	"""binary tree"""
	def __init__(self,key):
		self.root = BinaryTreeNode(key)
	def add(self, value, parentValue):
		parent = self.search(parentValue)
		if not parent:
			print("Parent not found")
			return
		node = BinaryTreeNode(value)
		if not parent.left_child:
			parent.left_child = node
			node.parent = parent
		elif not parent.right_child:
			parent.right_child = node
			node.parent = node
		else:
			print("Parent has two children, node not added")


	def delete(self,value):
		node = self.search(value)
		if not node:
			print("Node not found")
			return
		if node.left_child or node.right_child:
			print("Node not deleted, has children")
			return
		if node.parent.left_child.key == value:
			node.parent.left_child = None
		elif node.parent.right_child.key == value:
			node.parent.right_child = None
		return

	def printTree(self):
		nodes = []
		nodes.append(self.root)
		while len(nodes):
			node = nodes.pop()
			print(node.key)
			if node.right_child:
				nodes.append(node.right_child)
			if node.left_child:
				nodes.append(node.left_child)

	def search(self,value):
		nodes = []
		nodes.append(self.root)
		while len(nodes):
			node = nodes[0]
			if node.key == value:
				return node
			if node.left_child:
				nodes.append(node.left_child)
			if node.right_child:
				nodes.append(node.right_child)
			nodes.pop(0)
		return None

class BinaryTreeNode():
	"""binary tree node"""
	def __init__(self,key):
		self.key = key
		self.left_child = None
		self.right_child = None
		parent = None

class Graph():
	"""dictionary graph"""
	def __init__(self,starting):
		self.vertices = {starting: []}

	def addVertex(self, value):
		if value in self.vertices:
			print("Vertex already exists")
		self.vertices[value] = []
	
	def addEdge(self,value1,value2):
		if (not(value1 in self.vertices)) or (not(value2 in  self.vertices)):
			print("One of more vertices not found")
			return
		self.vertices[value1].append(value2)
		self.vertices[value2].append(value1)

	def findVertex(self,value):
		if self.vertices[value]:
			print(self.vertices[value])
			return

### TESTING ###
## Queue Tests ##
print("Testing Queue...")
queue = newQueue()
for i in range(0,10):
	queue.put(i)
for i in range(0,10):
	print(queue.pop())
print("Finshed Queue Tests")

## Stack Tests ##
print("Testing Stack...")
stack = Stack()
for i in range(0,10):
	stack.push(i)
for i in range(0,10):
	print(stack.pop())
print("Finshed Stack Tests")

## Binary Tree Tests ##
print("Testing Binary Tree..")
tree = BinaryTree(0)
for i in range(1,11):
	tree.add(i,i-1)
print("Added 10 numbers")
tree.printTree()
tree.delete(10)
tree.delete(9)
print("Deleted node 10 and 9")
tree.printTree()
print("Finshed Tree Tests")

## Graph Tests ##
print("Testing Graph...")
graph = Graph(10)
for i in range(0,10):
	graph.addVertex(i)
print("Added 10 Verticies")
for i in range(0,10):
	graph.addEdge(i, (10 - i)/2)
	graph.addEdge(i, (10 - i)/3)
print("Added 20 Edges")
for i in range(0,5):
	graph.findVertex(i)
print("Found 5 Verticies")
print("Finshed Graph Tests")

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("FINISHED!")
