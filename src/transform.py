import math
from engine_types import Vector3, Coordinate3

class Transform:
    """
    Represents a 3D Transform in a computer-graphics enviroment

    A 3D Transform encapsulates position, rotation and scale in 3D space
    and provides an interface for manipulating these properties.

    Attributes:
        position
        rotation
        scale
    """
    def __init__(
            self,
            position: Vector3 = Vector3(x=0, y=0, z=0),
            rotation: Vector3 = Vector3(x=0, y=0, z=0),
            scale: Vector3 = Vector3(x=1, y=1, z=1)
        ) -> None:

        self.position = position
        self.rotation = rotation
        self.scale = scale

    def rotate_by(self, delta: Vector3) -> None:
        """ update rotation """
        self.rotation = Vector3(
            x = self.rotation.x + delta.x,
            y = self.rotation.y + delta.y,
            z = self.rotation.z + delta.z
        )

    def translate_by(self, delta: Vector3) -> None:
        """ update position """
        self.position = Vector3(
            x = self.position.x + delta.x,
            y = self.position.y + delta.y,
            z = self.position.z + delta.z
        )

    def scale_by(self, delta: Vector3) -> None:
        """ update scale """
        self.scale = Vector3(
            x = self.scale.x * delta.x,
            y = self.scale.y * delta.y,
            z = self.scale.z * delta.z
        )

    @staticmethod
    def rotate_vertex_xyz(v: Coordinate3, rotation: Vector3) -> Coordinate3:
        """
        rotate 3D vertex around x, y, z axis (euler rotation, local rotation)
        """
        # rotation is implemented with rotation-matrix.
        # for more information, look up https://en.wikipedia.org/wiki/Rotation_matrix
        sin_x, cos_x = math.sin(rotation.x), math.cos(rotation.x)
        sin_y, cos_y = math.sin(rotation.y), math.cos(rotation.y)
        sin_z, cos_z = math.sin(rotation.z), math.cos(rotation.z)

        # 1. rotate around x axis
        v = Coordinate3(
            x = v.x,
            y = v.y * cos_x - v.z * sin_x,
            z = v.y * sin_x + v.z * cos_x
        )

        # 2. rotate around y axis
        v = Coordinate3(
            x = v.x * cos_y - v.z * sin_y,
            y = v.y,
            z = v.x * sin_y + v.z * cos_y,
        )

        # 3. rotate around z axis
        v = Coordinate3(
            x = v.x * cos_z - v.y * sin_z,
            y = v.x * sin_z + v.y * cos_z,
            z = v.z
        )

        return v

    def apply_to_vertex(self, v: Coordinate3) -> Coordinate3:
        """
        Calculate and return transformed 3D world-space coordinate of vertex v
        """
        # 1. scale
        v = Coordinate3(
            x = v.x * self.scale.x,
            y = v.y * self.scale.y,
            z = v.z * self.scale.z
        )

        # 2. rotate
        v = self.rotate_vertex_xyz(v, self.rotation)

        # 3. translate
        v = Coordinate3(
            x = v.x + self.position.x,
            y = v.y + self.position.y,
            z = v.z + self.position.z
        )
        
        return v
