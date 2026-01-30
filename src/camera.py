from engine_types import Coordinate3

class Camera:
    def __init__(self, position: Coordinate3) -> None:
        self.camera_pos = position