#!/usr/bin/env python3
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

    def write(self, message, tag: str = ""):
        with self.lock.gen_wlock():
            print(f"{tag} has write lock")
            self.message = message
        print(f"{tag} let go of write lock")
        return

    def read(self, tag: str = ""):
        with self.lock.gen_rlock():
            print(f"{tag} has read lock")
            message = self.message
        print(f"{tag} let go of read lock")
        return message
