from enum import Enum


class HeroAreaEnum(Enum):
    FRONT = 1
    BACK = 2

    def __str__(self):
        return self.name


class Hero:

    def __init__(self, name: str, hp: float, defence: float, attack: float,
                 speed: float, area: HeroAreaEnum = HeroAreaEnum.BACK):
        self.name = name
        self.hp = hp
        self.defence = defence
        self.attack = attack
        self.speed = speed
        self.area = area
        self.is_alive = True

    def __repr__(self):
        return f'{self.name} with Hp: {self.hp}, area: {self.area}'


class Attack:

    def __init__(self, name, power, speed, cost=0, victim='target', sacrifice=0):
        self.name = name
        self.power = power
        self.speed = speed
        self.cost = cost
        self.victim = victim
        self.sacrifice = sacrifice
