# -*- coding: utf-8 -*-
"""This module contains methods and constants for clock ticks and timing."""

import time
import pygame

# Number of ticks per second.
CLOCK_TICK = 30

# Number of milliseconds in a second.
NUM_MS_SECOND = 1000

# Numer of ticks between refreshing map.
REFRESH_INTERVAL_NUM_TICKS = CLOCK_TICK

class Timekeeper(object):
    # Class pygame Clock object.
    clock = None

    # Number of ticks since the module was loaded.
    num_ticks = 0

    @classmethod
    def init_clock(cls):
        """Sets up the pygame Clock object."""

        Timekeeper.clock = pygame.time.Clock()

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

        Timekeeper.clock.tick(tick_amount)
        cls.num_ticks += 1

    @classmethod
    def time_ms(cls):
        """Returns the current system time in milliseconds."""

        return int(time.time_ns() / 1000)

    @classmethod
    def elapsed_ticks(cls):
        """Returns the number of ticks that elapsed since the module loaded."""

        return cls.num_ticks
