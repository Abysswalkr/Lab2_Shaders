from math import pi, sin, cos, isclose

def barycentricCoords(A, B, C, P):
	
	# Se saca el área de los subtriángulos y del triángulo
	# mayor usando el Shoelace Theorem, una fórmula que permite
	# sacar el área de un polígono de cualquier cantidad de vértices.

	areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
				  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

	areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

	areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

	areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

	# Si el área del triángulo es 0, retornar nada para
	# prevenir división por 0.
	if areaABC == 0:
		return None

	# Determinar las coordenadas baricéntricas dividiendo el 
	# área de cada subtriángulo por el área del triángulo mayor.
	u = areaPCB / areaABC
	v = areaACP / areaABC
	w = areaABP / areaABC


	# Si cada coordenada está entre 0 a 1 y la suma de las tres
	# es igual a 1, entonces son válidas.
	if 0<=u<=1 and 0<=v<=1 and 0<=w<=1 and isclose(u+v+w, 1.0):
		return (u, v, w)
	else:
		return None
	

def TranslationMatrix(x, y, z):
	
	return [
		[1, 0, 0, x],
		[0, 1, 0, y],
		[0, 0, 1, z],
		[0, 0, 0, 1]
	]

def ScaleMatrix(x, y, z):
	
	return [[x, 0, 0, 0],
			[0, y, 0, 0],
			[0, 0, z, 0],
			[0, 0, 0, 1]]

def RotationMatrix(pitch, yaw, roll):
	
	# Convertir a radianes
	pitch *= pi/180
	yaw *= pi/180
	roll *= pi/180
	
	# Creamos la matriz de rotación para cada eje.
	pitchMat = [[1,0,0,0],
			    [0,cos(pitch),-sin(pitch),0],
			    [0,sin(pitch),cos(pitch),0],
			    [0,0,0,1]]
	
	yawMat = [[cos(yaw),0,sin(yaw),0],
			  [0,1,0,0],
			  [-sin(yaw),0,cos(yaw),0],
			  [0,0,0,1]]
	
	rollMat = [[cos(roll),-sin(roll),0,0],
			   [sin(roll),cos(roll),0,0],
			   [0,0,1,0],
			   [0,0,0,1]]

	return matrix_multiply(matrix_multiply(pitchMat, yawMat), rollMat)


def matrix_multiply(A, B):
	# Verificar la compatibilidad de dimensiones
	if len(A[0]) != len(B):
		raise ValueError("The number of columns in array A must be equal to the number of rows in array B.")

	# Inicializar la matriz resultado con ceros
	result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]

	# Realizar la multiplicación de matrices
	for i in range(len(A)):  # Filas de A
		for j in range(len(B[0])):  # Columnas de B
			for k in range(len(B)):  # Filas de B / Columnas de A
				result[i][j] += A[i][k] * B[k][j]

	# Devolver la matriz resultado
	return result

def inversed_matrix(matrix):
	# Create an identity matrix of the same size as the input matrix
	n = len(matrix)
	identity = [[float(i == j) for i in range(n)] for j in range(n)]

	# Create an augmented matrix by appending the identity matrix
	augmented_matrix = [row[:] + identity_row[:] for row, identity_row in zip(matrix, identity)]

	# Apply Gaussian elimination
	for i in range(n):
		# Make the diagonal contain all 1's
		if augmented_matrix[i][i] == 0:
			# Find a row with a non-zero element in the current column
			for j in range(i + 1, n):
				if augmented_matrix[j][i] != 0:
					# Swap rows
					augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
					break
			else:
				# If no non-zero element is found, the matrix is singular
				return None

		# Normalize the current row
		factor = augmented_matrix[i][i]
		for k in range(2 * n):
			augmented_matrix[i][k] /= factor

		# Make all rows except the current row have a 0 in the current column
		for j in range(n):
			if i != j:
				factor = augmented_matrix[j][i]
				for k in range(2 * n):
					augmented_matrix[j][k] -= factor * augmented_matrix[i][k]

	# Extract the inverse matrix from the augmented matrix
	inverse_matrix = [row[n:] for row in augmented_matrix]
	return inverse_matrix


def vector_matrix_multiply(vector, matrix):
	# Check if the multiplication is possible
	if len(vector) != len(matrix):
		raise ValueError("The vector and matrix dimensions do not align for multiplication.")

	# Multiply the vector by the matrix
	result_vector = []
	for i in range(len(matrix[0])):  # Assuming matrix is well-formed (rectangular)
		result_vector.append(sum(vector[j] * matrix[j][i] for j in range(len(vector))))

	return result_vector


	