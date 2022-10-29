#Creating a few functions for matrix operations.

#Multiply a matrix by an integer.
def mult_scalar(matrix, scale):
	#Create a new matrix since the old one should not be modified
	newMatrix = list(matrix)

	#Multiply each number in the matrix one by one.
	for x in range(len(newMatrix)):
		for y in range(len(newMatrix[x])):
			newMatrix[x][y] *= scale
	
	return newMatrix

#Multiply a matrix by another matrix.
def mult_matrix(a, b):
	#If the dimensions of the matrix are not compatible.
	if(len(a[0]) != len(b)):
		return None
	
	#Given matrix a is m x n and matrix b is n x p, the resulting matrix is m x p.
	newMatrix = [[0 for x in range(len(b[0]))] for y in range(len(a))]

	#Dot product the nth row by the nth column and store the result in the new matrix.
	for x in range(len(a)):
		for y in range(len(b[0])):
			newMatrix[x][y] = sum(a[x][z] * b[z][y] for z in range(len(b)))
	
	return newMatrix


#Find the Euclidean distance between two vectors.
def euclidean_dist(a, b):
	return None if len(a) != len(b) else (sum((a[0][x] - b[0][x]) ** 2 for x in range(len(a[0])))) ** 0.5