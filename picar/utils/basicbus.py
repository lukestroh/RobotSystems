#!/usr/bin/env/python3
"""
basicbus.py
Luke Strohbehn
"""
from typing import Any


class BasicBus:
    def __init__(self) -> None:
        self.message: Any

    def write(self, message):
        self.message = message
        return

    def read(self):
        return self.message
