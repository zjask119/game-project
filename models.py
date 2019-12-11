from enum import Enum
from operator import attrgetter


class HeroAreaEnum(Enum):
    FRONT = 1
    BACK = 2

    def __str__(self):
        return self.name


class Team:

    def __init__(self, name, heroes=None):
        self.name = name
        self.energy = 8
        self.heroes = set()

        if isinstance(heroes, (list, tuple, set)):
            for hero in heroes:
                self.add_hero(hero)

    def add_hero(self, hero):
        assert isinstance(hero, Hero)
        self.heroes.add(hero)

    def get_all_heroes(self, sorted_by=None):
        heroes = list(self.heroes)
        if sorted_by:
            heroes = sorted(heroes, key=attrgetter(sorted_by), reverse=True)
        return heroes

    def get_alive_heroes(self, sorted_by=None):
        return [hero for hero in self.get_all_heroes(sorted_by) if hero.alive]

    def is_anybody_alive(self):
        return any([hero.alive for hero in self.get_all_heroes()])

    @property
    def num_of_alive_heroes(self):
        return len(self.get_alive_heroes())

    def __repr__(self):
        return (f'{self.name} with heroes:\n\t' +
                '\n\t'.join([str(hero) for hero in self.get_all_heroes()]))


class Hero:

    def __init__(self,  name: str, hp: float, defence: float,
                 speed: float, moves: list, area: HeroAreaEnum = HeroAreaEnum.BACK):
        self.name = name
        self.hp = hp
        self.defence = defence
        self.speed = speed
        self.moves = moves
        self.area = area
        self.alive = True

    def __repr__(self):
        return f'{self.name} with Hp: {self.hp}, def: {self.defence}, speed: {self.speed}, area: {self.area}'


class Attack:

    def __init__(self, name, power, speed, cost=0, victim='target', sacrifice=0):
        self.name = name
        self.power = power
        self.speed = speed
        self.cost = cost
        self.victim = victim
        self.sacrifice = sacrifice

    def __repr__(self):
        return f'{self.name}, power: {self.power}, cost: {self.cost}'
