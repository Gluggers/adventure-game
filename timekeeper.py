# -*- coding: utf-8 -*-
"""This module contains methods and constants for clock ticks and timing."""

import time
import pygame

# Number of ticks per second.
CLOCK_TICK = 30

# Number of milliseconds in a second.
NUM_MS_SECOND = 1000

# Number of milliseconds per clock tick.
MS_PER_TICK = NUM_MS_SECOND // CLOCK_TICK

# Number of ticks between refreshing map.
REFRESH_INTERVAL_NUM_TICKS = 30

# Number of ticks between reblitting overworld.
OW_REBLIT_INTERVAL_NUM_TICKS = 3

class Timekeeper(object):
    """Handles time-based methods and functions, such as ticks.

    The user should not generate Timekeeper objects, as the class
    is primarily for class methods related to time and the
    pygame clock.
    """

    # Class pygame Clock object.
    _clock = None

    @classmethod
    def init_clock(cls):
        """Sets up the pygame Clock object."""

        cls._clock = pygame.time.Clock()

    @classmethod
    def tick(cls, tick_amount=CLOCK_TICK):
        """Have the class Clock object tick.

        Args:
            cls: class object.
            tick_amount: integer to determine the tick length. Higher tick
                means pausing for a shorter amount of time (time paused is
                approximately equal to 1 second / tick_amount).
                Defaults to 30 ticks per second.
        """

        cls._clock.tick(tick_amount)
