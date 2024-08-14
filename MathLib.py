from math import pi, sin, cos, isclose

def barycentricCoords(A, B, C, P):

    # Cálculo de las áreas usando el Teorema del Zapatero
    areaPCB = abs((P[0] * C[1] + C[0] * B[1] + B[0] * P[1]) -
                  (P[1] * C[0] + C[1] * B[0] + B[1] * P[0]))

    areaACP = abs((A[0] * C[1] + C[0] * P[1] + P[0] * A[1]) -
                  (A[1] * C[0] + C[1] * P[0] + P[1] * A[0]))

    areaABP = abs((A[0] * B[1] + B[0] * P[1] + P[0] * A[1]) -
                  (A[1] * B[0] + B[1] * P[0] + P[1] * A[0]))

    areaABC = abs((A[0] * B[1] + B[0] * C[1] + C[0] * A[1]) -
                  (A[1] * B[0] + B[1] * C[0] + C[1] * A[0]))

    # Evitar división por 0
    if areaABC == 0:
        return None

    # Cálculo de coordenadas baricéntricas
    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC

    # Verificar que las coordenadas sean válidas
    if 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1 and isclose(u + v + w, 1.0):
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

    return [
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ]


def RotationMatrix(pitch, yaw, roll):

    # Convertir grados a radianes
    pitch = pi / 180 * pitch
    yaw = pi / 180 * yaw
    roll = pi / 180 * roll

    # Matrices de rotación para cada eje
    pitchMat = [
        [1, 0, 0, 0],
        [0, cos(pitch), -sin(pitch), 0],
        [0, sin(pitch), cos(pitch), 0],
        [0, 0, 0, 1]
    ]

    yawMat = [
        [cos(yaw), 0, sin(yaw), 0],
        [0, 1, 0, 0],
        [-sin(yaw), 0, cos(yaw), 0],
        [0, 0, 0, 1]
    ]

    rollMat = [
        [cos(roll), -sin(roll), 0, 0],
        [sin(roll), cos(roll), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

    # Multiplicar las matrices de rotación
    return matrix_multiply(matrix_multiply(pitchMat, yawMat), rollMat)


def matrix_multiply(A, B):

    if len(A[0]) != len(B):
        raise ValueError("The number of columns in the first array must be equal to the number of rows in the second array.")

    # Inicializar la matriz resultado
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]

    # Multiplicar las matrices
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]

    return result


def inversed_matrix(matrix):

    n = len(matrix)

    # Crear matriz identidad
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    # Crear la matriz aumentada
    aumented_matrix = [row + identity_row for row, identity_row in zip(matrix, identity)]

    # Aplicar eliminación gaussiana
    for i in range(n):
        pivot = aumented_matrix[i][i]
        if pivot == 0:
            raise ValueError("Matrix is not invertible.")

        for j in range(2 * n):
            aumented_matrix[i][j] /= pivot

        for k in range(n):
            if k != i:
                factor = aumented_matrix[k][i]
                for j in range(2 * n):
                    aumented_matrix[k][j] -= factor * aumented_matrix[i][j]

    # Extraer la matriz inversa
    inverse_matrix = [row[n:] for row in aumented_matrix]

    return inverse_matrix


def vector_matrix_multiply(vector, matrix):

    if len(matrix[0]) != len(vector):
        raise ValueError("The number of columns in the array must match the size of the vector.")

    result = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(vector)):
            result[i] += matrix[i][j] * vector[j]

    return result
