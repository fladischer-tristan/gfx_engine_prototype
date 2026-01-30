from engine_types import Vector3, Coordinate3, MeshType
from mesh import Mesh

class PhysicsEngine:
    def __init__(self):
        self.mass = 1
        self.velocity = Vector3(x=0, y=0, z=0)
        self.acceleration = Vector3(x=0, y=0, z=0)

    @staticmethod
    def vertex_intersects_mesh(p: Coordinate3, mesh: Mesh) -> bool:
        x_min, x_max, y_min, y_max, z_min, z_max = 0, 0, 0, 0, 0, 0

        # Get min and max values of x, y, z axis
        for v in mesh:
            # X
            if v.x < x_min:
                x_min = v.x
            elif v.x > x_max:
                x_max = v.x
            # Y
            if v.y < y_min:
                y_min = v.y
            elif v.y > y_max:
                y_max = v.y
            # Z
            if v.z < z_min:
                z_min = v.z
            elif v.z > z_max:
                z_max = v.z

        # Check if point p is within min/max constrains
        x_valid = True if x_min <= p.x and p.x <= x_max else False
        y_valid = True if y_min <= p.y and p.y <= y_max else False
        z_valid = True if z_min <= p.z and p.z <= z_max else False

        return not (x_valid and y_valid and z_valid)
    
    def mesh_intersects_mesh(self, mesh1: list[Coordinate3], mesh2: list[Coordinate3]) -> bool:
        """ Return True if mesh1 intersects mesh2 (or vice versa)"""
        intersection = False
        
        for v in mesh1:
            if self.vertex_intersects_mesh(v, mesh2):
                intersection = True
                break
        return intersection

if __name__ == "__main__":
    phyEng = PhysicsEngine()

    p = Coordinate3(x=2, y=3, z=5)
    mockMesh = Mesh(MeshType.CUBE).vertices
    mockMesh2 = Mesh(MeshType.CUBE).vertices

    print(phyEng.mesh_intersects_mesh(mockMesh, mockMesh2))