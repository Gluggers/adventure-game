import pygame

CLOCK_TICK = 30

class Timekeeper():
    clock = None

    def __init__(self):
        self.clock_tick = CLOCK_TICK

    @classmethod
    def init_clock(cls):
        Timekeeper.clock = pygame.time.Clock()

    @classmethod
    def tick(cls):
        Timekeeper.clock.tick(CLOCK_TICK)
