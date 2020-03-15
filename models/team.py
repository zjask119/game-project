from operator import attrgetter

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

    def get_all_heroes(self, sorted_by='speed'):
        heroes = list(self.heroes)
        if sorted_by:
            heroes = sorted(heroes, key=attrgetter(sorted_by), reverse=True)
        return heroes

    def get_alive_heroes(self, sorted_by='speed'):
        return [hero for hero in self.get_all_heroes(sorted_by) if hero.alive]

    def is_anybody_alive(self):
        return any([hero.alive for hero in self.get_all_heroes()])

    @property
    def num_of_alive_heroes(self):
        return len(self.get_alive_heroes())

    def __repr__(self):
        return (f'{self.name} with heroes:\n\t' +
                '\n\t'.join([str(hero) for hero in self.get_all_heroes()]))
