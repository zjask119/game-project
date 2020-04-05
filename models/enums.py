from enum import Enum


class HeroAreaEnum(Enum):
    FRONT = 1
    BACK = 2

    def __str__(self):
        return self.name.lower()
