# -*- coding: utf-8 -*-
"""Contains constants for currency.

Defines the following:
    - Currency types.
    - mapping of currency types to their values.
"""

### CURRENCY TYPES ###
CURRENCY_GOLD_COIN = 0x1
CURRENCY_SILVER_COIN = 0x2
CURRENCY_TRADING_STICKS = 0x3
CURRENCY_YEN = 0x4

# Maps currency IDs to the number of units equivalent to 1 Base Value
CURRENCY_VALUE_MAPPING = {
    CURRENCY_GOLD_COIN: 1,
    CURRENCY_SILVER_COIN: 3,
    CURRENCY_TRADING_STICKS: 5,
    CURRENCY_YEN: 2,
}
