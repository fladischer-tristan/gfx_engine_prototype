from engine_types import MeshType, Coordinate3

"""
dictionary for storing mesh data of GameObjects (eg. Cube, Octahedron)
"""
mesh_table = {
    "CUBE" : {
        "vertices" : (
            Coordinate3(-1, -1, -1), # front-bottom-left
            Coordinate3(-1,  1, -1), # front-top-left
            Coordinate3( 1,  1, -1), # front-top-right
            Coordinate3( 1, -1, -1), # front-bottom-right
            Coordinate3(-1, -1,  1), # back-bottom-left
            Coordinate3(-1,  1,  1), # back-top-left
            Coordinate3( 1,  1,  1), # back-top-right
            Coordinate3( 1, -1,  1)  # back-bottom-right
        ),

        "edges" : (
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ),

        "faces" : (
            (0, 3, 7, 4),  # bottom
            (3, 2, 6, 7), # right
            (7, 6, 5, 4), # back
            (0, 1, 2, 3), # front
            (4, 5, 1, 0), # left
            (1, 5, 6, 2)  # top
        )
    },

    "PYRAMID" : {
        "vertices": (
            Coordinate3(-1, -1, -1), # front-bottom-left
            Coordinate3(1, -1, -1),  # front-bottom-right
            Coordinate3(1, -1, 1),   # back-bottom-right
            Coordinate3(-1, -1, 1),  # back-bottom-left
            Coordinate3(0, 1, 0)     # top
        ),

        "edges": (
            (0, 1), (1, 2), (2, 3), (3, 0),
            (0, 4), (1, 4), (2, 4), (3, 4)
        ),

        "faces": (
            (0, 1, 2, 3), (0, 4, 1), (1, 4, 2), 
            (2, 4, 3), (3, 4, 0)
        )
    },

    "OCTAHEDRON" : {
        "vertices" : (
            Coordinate3(-1, 0, -1), # front left
            Coordinate3(1, 0, -1),  # front right
            Coordinate3(-1, 0, 1),  # back left
            Coordinate3(1, 0, 1),   # back right
            Coordinate3(0, 1, 0),   # top
            Coordinate3(0, -1, 0),  # bottom
        ),

        "edges" : (
            (0, 1), (1, 3), (0, 2), (2, 3),
            (0, 4), (1, 4), (2, 4), (3, 4),
            (0, 5), (1, 5), (2, 5), (3, 5),
        ),

        "faces" : (
            (0, 4, 1),
            (1, 4, 3),
            (3, 4, 2),
            (2, 4, 0),
            (0, 1, 5),
            (1, 3, 5),
            (3, 2, 5),
            (2, 0, 5)
        )
    }
}

class Mesh:
    """
    Stores mesh data of GameObject

    Attributes:
        vertices
        edges
        faces
    """
    def __init__(self, mesh_type: MeshType) -> None:
        # choose right mesh for corresponding MeshType
        data = mesh_table[mesh_type.value]
        self.vertices = data["vertices"]
        self.edges = data["edges"]
        self.faces = data["faces"]