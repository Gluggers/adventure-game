import pygame
import time

CLOCK_TICK = 30
NUM_MS_SECOND = 1000

# Numer of ticks between refreshing map.
REFRESH_INTERVAL_NUM_TICKS = CLOCK_TICK

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

    @classmethod
    def time_ms(cls):
        return int(time.time_ns() / 1000)
