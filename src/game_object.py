from engine_types import Coordinate3, Vector3, MeshType, Face3, Edge3
from physics import PhysicsEngine
from transform import Transform
from mesh import Mesh

class GameObject:
    def __init__(self, name: str, type: MeshType, position: Vector3, rotation: Vector3, scale: Vector3):
        """
        Instantiates 3D Cube object

        Attributes:
            name
            transform
            type
            mesh
            physics_engine
        """
        self.name = name
        self.transform = Transform(position, rotation, scale)
        self.type = type
        self.mesh = Mesh(type)
    
    ##################################################################################
    ################################ public interface ################################
    ##################################################################################

    def transform_vertex(self, v: Coordinate3) -> Coordinate3:
        """ Compute and return world coordinate of single vertex"""
        return self.transform.apply_to_vertex(v)
    
    def transform_edge(self, e: Edge3) -> Edge3:
        transformed_vertices = []
        for i in e:
            v = self.mesh.vertices[i] # Since Edge3 is made of indicies, we map to the vertex v
            transformed_vertices.append(self.transform_vertex(v))
        return tuple(transformed_vertices)
    
    def transform_face(self, f: Face3) -> Face3:
        """ Compute and return world coordinates of Face3 """
        transformed_vertices = []
        for i in f:
            v = self.mesh.vertices[i] # Since Face3 is made of indicies, we map to the vertex v
            transformed_vertices.append(self.transform_vertex(v))
        return tuple(transformed_vertices)

    def transform_game_object(self) -> list[Coordinate3]:
        """ Compute and return all world-coordinates of a GameObject """
        transformed_vertices = []
        for v in self.mesh.vertices:
            # Loop over all vertices and perform transform
            transformed_vertices.append(self.transform_vertex(v))
        return transformed_vertices

    def move_right(self, distance: float) -> None:
        """ Translate GameObject's transform on positive x axis """
        self.transform.translate_by(Vector3(x=distance, y=0, z=0))
        
    def move_left(self, distance: float) -> None:
        """ Translate GameObject's transform on negative x axis """
        self.transform.translate_by(Vector3(x=-distance, y=0, z=0))

    def move_up(self, distance: float) -> None:
        """ Translate GameObject's transform on positive y axis """
        self.transform.translate_by(Vector3(x=0, y=distance, z=0))

    def move_down(self, distance: float) -> None:
        """ Translate GameObject's transform on negative y axis """
        self.transform.translate_by(Vector3(x=0, y=-distance, z=0))

    def move_front(self, distance: float) -> None:
        """ Translate GameObject's transform on positive z axis """
        self.transform.translate_by(Vector3(x=0, y=0, z=distance))

    def move_back(self, distance: float) -> None:
        """ Translate GameObject's transform on negative z axis """
        self.transform.translate_by(Vector3(x=0, y=0, z=-distance))

    def rotate_x(self, angle : float) -> None:
        """ Rotate GameObject's transform around x axis locally"""
        self.transform.rotate_by(Vector3(x=angle, y=0, z=0))

    def rotate_y(self, angle : float) -> None:
        """ Rotate GameObject's transform around y axis locally"""
        self.transform.rotate_by(Vector3(x=0, y=angle, z=0))

    def rotate_z(self, angle : float) -> None:
        """ Rotate GameObject's transform around z axis locally"""
        self.transform.rotate_by(Vector3(x=0, y=0, z=angle))