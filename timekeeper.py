import pygame

CLOCK_TICK = 30
NUM_MS_SECOND = 1000

class Timekeeper():
    clock = None

    def __init__(self):
        self.clock_tick = CLOCK_TICK

    @classmethod
    def init_clock(cls):
        Timekeeper.clock = pygame.time.Clock()

    @classmethod
    def tick(cls, tick_amount=CLOCK_TICK):
        Timekeeper.clock.tick(tick_amount)
