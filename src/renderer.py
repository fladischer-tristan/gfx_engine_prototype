import pygame
from game_object import GameObject
from engine_types import Vector3, Coordinate3, Face3
import math

camera_pos = Coordinate3(0, 0, 0) # static camera for now - NOTE: will be refactored into seperate class later

def normalize_vector3(v: Vector3) -> Vector3:
    """ Normalize Vector3 """
    mag = math.sqrt((v.x**2) + (v.y**2) + (v.z**2)) # Get magnitude of vector

    if mag == 0.0:
        return Vector3(x=0, y=0, z=0) # since we cannot divide by zero

    inv_mag = 1.0 / mag

    return Vector3(
        x = v.x * inv_mag,
        y = v.y * inv_mag,
        z = v.z * inv_mag
    )

def compute_face_center(f: Face3) -> Coordinate3:
    """ Compute and return center Coordinate3 of face. Face needs at least 3 vertices """
    length = len(f)
    if length < 3:
        raise ValueError("Face needs at least 3 vertices")
    center = Coordinate3(x=0, y=0, z=0)
    # Sum up all vertices v in face:
    for v in f:
        center += v
    return center * (1 / length) # finally multiply by 1 / length

def cross_vector3(a: Vector3, b: Vector3) -> Vector3:
    """ Compute cross product of Vector3's a and b """
    return Vector3 (
        x = a.y * b.z - a.z * b.y,
        y = a.z * b.x - a.x * b.z,
        z = a.x * b.y - a.y * b.x
    )

def dot_vector3(a: Vector3, b: Vector3) -> float:
    """ Compute dot product of Vector3's a and b"""
    return a.x * b.x + a.y * b.y + a.z * b.z

def compute_face_normal(f: Face3) -> Vector3:
    """ Compute the normal of a face  """
    if len(f) < 3:
        raise ValueError("Face needs at least 3 vertices")
    p0, p1, p2, *rest = f # *rest allows faces of more than 3 vertices to be passed in. (3 is all you need)
    e1 = Vector3(p1.x - p0.x, p1.y - p0.y, p1.z - p0.z)
    e2 = Vector3(p2.x - p0.x, p2.y - p0.y, p2.z - p0.z)
    return normalize_vector3(cross_vector3(e1, e2))

def is_backface(face: Face3) -> bool:
    c = compute_face_center(face)
    N = compute_face_normal(face)
    V = Vector3(camera_pos.x - c.x, camera_pos.y - c.y, camera_pos.z - c.z)
    return dot_vector3(N, V) <= 0.0


def project(coor : list | tuple) -> tuple:
    """
    project 3D point into 2D space

    parameters:
        coor: list or tuple of [x, y, z]
    """
    x, y, z = coor

    # project x and y to 3D space if z is not 0
    if z != 0:
        x = x / z
        y = y / z
    else:
        # avoid division by zero
        raise ZeroDivisionError("division by zero in projection function.")

    return (x, y)

def scale(coordinate : list | tuple, SCREEN_WIDTH: int, SCREEN_HEIGHT: int) -> tuple:
    """
    scale 2D point from [-1; 1] to [0; SCREEN_WIDTH / SCREEN_HEIGHT]

    parameters:
        - coordinate: list or tuple of elements [x, y]
    """
    x, y = coordinate # x in range [-1; 1], y in range[-1; 1]
    y *= -1 # invert y since pygame uses standard gfx coor system
    x = (x + 1) / 2 # [0; 1]
    y = (y + 1) / 2 # [0; 1]
    x *= SCREEN_WIDTH # [0; SCREEN_WIDTH]
    y *= SCREEN_HEIGHT # [0; SCREEN_HEIGHT]

    return (x, y)

def render_object(screen: pygame.Surface, game_object: GameObject, color: str = "red", radius: int = 1) -> None:
    """
    Render GameObject to pygame screen
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()

    coordinates = game_object.transform_game_object()

    for face in game_object.mesh.faces:
        world_face = tuple(coordinates[index] for index in face)

        if is_backface(world_face):
            continue
        else:
            projected_face = tuple(scale(project(p), screen_width, screen_height) for p in world_face)
            pygame.draw.polygon(screen, "red", projected_face)

            world_face = tuple(coordinates[index] for index in face)

            # DEBUG: render lines included in that face, to check if backface culling is working
            # if it works, no hidden lines should be rendered
            for edge in game_object.mesh.edges:
                idx1, idx2 = edge
                if idx1 in face and idx2 in face:
                    #print(f"Success! edge: {edge} in face: {face}")
                    start_idx = edge[0]
                    end_idx = edge[1]
                    start = scale(project(coordinates[start_idx]), screen_width, screen_height)
                    end = scale(project(coordinates[end_idx]), screen_width, screen_height)
                    pygame.draw.line(screen, "blue", start, end)

                    # also draw vertices at the end
                    pygame.draw.circle(screen, "green", start, radius)
                    pygame.draw.circle(screen, "green", end, radius)
                    #print(f"edge: {edge} not in face: {face}")




    # for face in obj.mesh.faces:
    #     polygons = [scale(project(coordinates[idx]), screen_width, screen_height) for idx in face]
    #     pygame.draw.polygon(screen, "red", polygons)

    # for edge in obj.mesh.edges:
    #     start_idx = edge[0]
    #     end_idx = edge[1]
    #     start = scale(project(coordinates[start_idx]), screen_width, screen_height)
    #     end = scale(project(coordinates[end_idx]), screen_width, screen_height)
    #     pygame.draw.line(screen, "blue", start, end)

    # for coor in coordinates:
    #     coor = scale(project(coor), screen_width, screen_height)
    #     pygame.draw.circle(screen, "green", coor, 1)