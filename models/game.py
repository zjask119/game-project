from operator import attrgetter
from random import choice

from displayer import print_error, print_heroes
from models.enums import HeroAreaEnum


class Game:

    def __init__(self, team1, team2):
        from models.team import Team
        assert isinstance(team1, Team)
        assert isinstance(team2, Team)
        self.teams = [team1, team2]
        self.round = 0

    def get_all_heroes(self, sorted_by='speed'):
        heroes = []
        for team in self.teams:
            heroes.extend(team.get_all_heroes(sorted_by=None))

        heroes = sorted(heroes, key=attrgetter(sorted_by), reverse=True)
        return heroes

    def get_alive_heroes(self, sorted_by='speed'):
        return [hero for hero in self.get_all_heroes(sorted_by) if hero.alive]

    @staticmethod
    def ask_number(values):
        while True:
            try:
                print(f'\nChoose between 1 - {len(values)}.')
                index = int(input('Your Choice is: '))
                print()
            except ValueError:
                print_error('Given number is not valid! Try again.')
                continue
            if index in range(1, len(values) + 1):
                return index

    @staticmethod
    def choose_target(attacking_team, enemy_team=None):
        if enemy_team:
            heroes = enemy_team.get_alive_heroes()
        else:
            heroes = attacking_team.get_alive_heroes()

        if attacking_team.npc:
            return Game.random_target(heroes)

        print('\nChoose target:')
        print_heroes(heroes)
        num = Game.ask_number(heroes)
        if any(hero.area == HeroAreaEnum.FRONT for hero in heroes):
            while heroes[num - 1].area != HeroAreaEnum.FRONT:
                print(f'Cannot attack {heroes[num - 1].name} now.')
                print('First eliminate warriors from the front area.')
                num = Game.ask_number(heroes)
            return heroes[num - 1]
        else:
            return heroes[num - 1]

    @staticmethod
    def random_target(heroes):
        front_line = [hero for hero in heroes if hero.area == HeroAreaEnum.FRONT]
        if front_line:
            victim = choice(front_line)
        else:
            victim = choice(heroes)
        return victim

    def prepare_round(self, team_energy):
        for team in self.teams:
            team.reduce_heroes_attributes()
            team.set_energy(team_energy)
        for hero in self.get_all_heroes():
            hero.reset_shield()
            hero.self_recovery()

    def reset_attributes(self):
        for hero in self.get_all_heroes():
            hero.victim = False
            hero.active = False
