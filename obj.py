class Obj(object):
    def __init__(self, filename):
        # Asumiendo que el archivo es un formato .obj
        with open(filename, "r") as file:
            lines = file.read().splitlines()

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        for line in lines:
            # Este comando elimina espacios en blanco innecesarios
            # al final de un texto
            line = line.rstrip()

            # Si la linea no cuenta con un prefijo y un valor,
            # seguimos a la siguiente la linea
            if not line or line.startswith("#"):
                continue

            try:
                prefix, value = line.split(" ", 1)
            except ValueError:
                continue

            # Dependiendo del prefijo, parseamos y guardamos
            # la informacion en el contenedor correcto
            if prefix == "v":  # Vertices
                vert = list(map(float, value.split(" ")))
                self.vertices.append(vert)

            elif prefix == "vt":  # Coordenadas de textura
                vts = list(map(float, value.split(" ")))
                self.texcoords.append([vts[0], vts[1]])

            elif prefix == "vn":  # Normales
                norm = list(map(float, value.split(" ")))
                self.normals.append(norm)

            elif prefix == "f":  # Caras
                face = []
                verts = value.split(" ")
                for vert in verts:
                    # Split vertex information and handle missing values
                    vertex_info = [int(v) if v else None for v in vert.split("/")]

                    # Default missing values to 0 (or any other appropriate default)
                    while len(vertex_info) < 3:
                        vertex_info.append(None)  # Adding None for missing texture/normal data

                    face.append(vertex_info)
                self.faces.append(face)