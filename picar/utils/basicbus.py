#!/usr/bin/env/python3
"""
basicbus.py
Luke Strohbehn
"""
from typing import Any
from readerwriterlock import rwlock


class BasicBus:
    def __init__(self) -> None:
        self.message: Any
        self.lock = rwlock.RWLockWriteD()

    def write(self, message):
        with self.lock.gen_wlock():
            self.message = message
        return

    def read(self):
        with self.lock.gen_rlock():
            message = self.message
        return message
