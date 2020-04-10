from operator import attrgetter

from models.enums import HeroAreaEnum
from models.hero import Hero


class Team:

    def __init__(self, name, npc, heroes=None):
        self.name = name
        self.energy = 0
        self.heroes = set()
        self.npc = npc

        if isinstance(heroes, (list, tuple, set)):
            for hero in heroes:
                self.add_hero(hero)

    def add_hero(self, hero):
        assert isinstance(hero, Hero)
        hero.team = self
        self.heroes.add(hero)

    def get_all_heroes(self, area=None, sorted_by='speed'):
        heroes = list(self.heroes)
        if area:
            assert type(area) is HeroAreaEnum
            heroes = [hero for hero in heroes if hero.area == area]
        if sorted_by:
            heroes = sorted(heroes, key=attrgetter(sorted_by), reverse=True)
        return heroes

    def get_alive_heroes(self, area=None, sorted_by='speed'):
        heroes = [hero for hero in self.get_all_heroes(area, sorted_by) if hero.alive]
        return heroes

    def is_anybody_alive(self):
        return any(self.get_alive_heroes())

    @property
    def num_of_alive_heroes(self):
        return len(self.get_alive_heroes())

    def set_energy(self, points):
        self.energy = points

    def reduce_heroes_attributes(self):
        for hero in self.get_all_heroes():
            hero.update_attributes()

    def __repr__(self):
        return (f'{self.name} with heroes:\n\t' +
                '\n\t'.join([str(hero) for hero in self.get_all_heroes()]))
