from MathLib import matrix_multiply, vector_matrix_multiply, barycentricCoords


def vertexShader(vertex, **kwargs):

    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]

    # Agregar el componente W al vértice
    vt = [vertex[0], vertex[1], vertex[2], 1]

    # Transformar el vértice por las matrices en el orden correcto
    vt = vector_matrix_multiply(vt, matrix_multiply(
        matrix_multiply(
            matrix_multiply(viewportMatrix, projectionMatrix),
            viewMatrix),
        modelMatrix))

    # Normalizar las coordenadas homogéneas si es necesario
    vt = [vt[0] / vt[3], vt[1] / vt[3], vt[2] / vt[3]]

    return vt


def fragmentShader(**kwargs):

    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs.get("texture", None)
    dirLight = kwargs["dirLight"]

    # Interpolar las coordenadas de textura y normales
    interpolatedTexCoords = [
        u * A[3] + v * B[3] + w * C[3],  # Asumiendo que A, B, C tienen coordenadas de textura en el índice 3
        u * A[4] + v * B[4] + w * C[4]  # Asumiendo que A, B, C tienen normales en el índice 4
    ]

    # Si hay una textura, obtener el color de la textura y aplicarlo
    if texture:
        texColor = texture.get_color(interpolatedTexCoords)  # Método get_color de la textura
    else:
        texColor = [1, 1, 1]  # Color blanco por defecto si no hay textura

    # Aplicar la dirección de la luz y la textura interpolada
    color = [
        texColor[0] * dirLight[0],
        texColor[1] * dirLight[1],
        texColor[2] * dirLight[2]
    ]

    return color


def flatShader(**kwargs):

    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs.get("texture", None)
    dirLight = kwargs["dirLight"]

    # Interpolar las coordenadas de textura
    interpolatedTexCoords = [
        u * A[3] + v * B[3] + w * C[3],
        u * A[4] + v * B[4] + w * C[4]
    ]

    # Si hay una textura, obtener el color de la textura y aplicarlo
    if texture:
        texColor = texture.get_color(interpolatedTexCoords)
    else:
        texColor = [1, 1, 1]  # Blanco por defecto si no hay textura

    # Devolver el color sin aplicar efectos adicionales (flat shading)
    color = [
        texColor[0] * dirLight[0],
        texColor[1] * dirLight[1],
        texColor[2] * dirLight[2]
    ]

    return color
