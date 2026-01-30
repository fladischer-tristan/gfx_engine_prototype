"""
Author: Tristan Fladischer

Small GFX/Game engine prototype

implements features like:
    3D - 2D projection
    matrix rotation on 3D objects
    Transforms & basic collisions (wip)
    Meshes for 3 Objects (Cube, Pyramid, Octahedron)
    custom types
    user input (wip)
    camera (wip)
    backface culling

TODO:
    InputHandler class
    Pyhsics Manager
    Engine class

    features that may be implemented, depending on scalability:
        culling (z plane)
        anti aliasing (smoothing stair-like edges using contrasts)
        camera clipping
        camera movement (maybe a Camera class)
        Terminal support (interface for creating/manipulating game objects at runtime)

    NOTE: This file should only include "game.start()" at some point. Everything else should be refactored
          into seperate files/classes/modules for readability and flexibility
"""
import random
import pygame
from game_object import GameObject
import renderer
from physics import PhysicsEngine
from engine_types import Vector3, MeshType

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
INPUT_MOVE_WEIGHT, INPUT_ROTATION_WEIGHT = 0.1, 0.01 # weights for movement/rotation

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True # gameloop flag

game_object_list = []

# #instantiating random gameobjectss
# for i in range(20):
#     mesh_int = random.randint(0, 2)
#     mesh_type = MeshType.CUBE
#     match mesh_int:
#         case 0: mesh_type = MeshType.CUBE
#         case 1: mesh_type = MeshType.PYRAMID
#         case 2: mesh_type = MeshType.OCTAHEDRON

#     position = Vector3(x=random.randint(-10, 10), y=random.randint(-10, 10), z=random.randint(20, 40))
#     rotation = Vector3(x=random.randint(-6, 6), y=random.randint(-6, 6), z=random.randint(-6, 6))
#     scale = Vector3(x=random.randint(-4, 4), y=random.randint(-4, 4), z=random.randint(-6, 6))
#     new_obj = GameObject("GO", mesh_type, position, rotation, scale)
#     game_object_list.append(new_obj)

physicsEngine = PhysicsEngine()

player = GameObject("player", MeshType.PYRAMID, Vector3(1, 2, 20), Vector3(0, 0, 0), Vector3(1, 1, 1))
game_object_list.append(player)

ground = GameObject("ground", MeshType.CUBE, Vector3(0, -1, 20), Vector3(0, 0, 0), Vector3(10, 0.1, 10))
game_object_list.append(ground)

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    # clean screen before rendering
    screen.fill("black")
    clock.tick(1000)
    #print(clock.get_fps())

    # render objects
    for obj in game_object_list:
        if obj.name == "player":
            mesh1 = obj.transform_game_object()
            mesh2 = game_object_list[1].transform_game_object()

            intersects = physicsEngine.mesh_intersects_mesh(mesh1, mesh2)
            print(intersects)
            if intersects:
                # update position
                if keys[pygame.K_a]:
                    obj.move_left(INPUT_MOVE_WEIGHT)
                if keys[pygame.K_d]:
                    obj.move_right(INPUT_MOVE_WEIGHT)
                if keys[pygame.K_w]:
                    obj.move_front(INPUT_MOVE_WEIGHT)
                if keys[pygame.K_s]:
                    obj.move_back(INPUT_MOVE_WEIGHT)
                if keys[pygame.K_q]:
                    obj.move_up(INPUT_MOVE_WEIGHT)
                if keys[pygame.K_e]:
                    obj.move_down(INPUT_MOVE_WEIGHT)
                
                # rotation
                if keys[pygame.K_x]:
                    obj.rotate_x(INPUT_ROTATION_WEIGHT)
                if keys[pygame.K_y]:
                    obj.rotate_y(INPUT_ROTATION_WEIGHT)
                if keys[pygame.K_z]:
                    obj.rotate_z(INPUT_ROTATION_WEIGHT)
                # if obj.name != "playerCube":
                #     obj.rotate_x(INPUT_ROTATION_WEIGHT)
                #     obj.rotate_y(INPUT_ROTATION_WEIGHT)
                # render everything to pygame screen
        renderer.render_object(screen, obj, "green", 1)
    pygame.display.flip()
    pygame.time.delay(10)
pygame.quit()