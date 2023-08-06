from .exceptions import *


class Manager:

    def __init__(self):
        self.objects = []

    def set_cls(self, cls):
        """The Parser object tells the manager to use it"""
        self.cls = cls

    def create(self, **kwargs):
        """Create and save object"""
        cls = self.cls
        obj = cls(**kwargs)
        self.append(obj)

    def all(self):
        return self.objects

    def append(self, obj):
        self.objects.append(obj)

    def count(self):
        return len(self.objects)
