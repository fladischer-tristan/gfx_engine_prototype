"""
Detects and processes user-input over keyboard and terminal
"""

import pygame

class InputHandler:
    def __init__(self):
        raise NotImplementedError

    def get_key_state() -> list:
        return pygame.key.get_pressed()
    
    def disptach_keys() -> None:
        pass


