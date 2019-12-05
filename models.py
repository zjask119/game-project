from enum import Enum


class HeroAreaEnum(Enum):
    FRONT = 1
    BACK = 2

    def __str__(self):
        return self.name


class Hero:

    def __init__(self, id: int,  name: str, hp: float, defence: float,
                 speed: float, moves: list, area: HeroAreaEnum = HeroAreaEnum.BACK):
        self.id = id
        self.name = name
        self.hp = hp
        self.defence = defence
        self.speed = speed
        self.moves = moves
        self.area = area
        self.is_alive = True

    def __repr__(self):
        return f'{self.name} with Hp: {self.hp}, area: {self.area}'


class Attack:

    def __init__(self, id: int, name, power, speed, cost=0, victim='target', sacrifice=0):
        self.id = id
        self.name = name
        self.power = power
        self.speed = speed
        self.cost = cost
        self.victim = victim
        self.sacrifice = sacrifice


    def __repr__(self):
        return f'{self.name}'
