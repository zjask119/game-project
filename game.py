from enums import HeroAreaEnum
from random import choice
from operator import attrgetter


class Game:

    def __init__(self, teams=None):
        self.teams = []
        if teams and isinstance(teams, list):
            for team in teams:
                self.add_team(team)

    def add_team(self, team):
        self.teams.append(team)

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
            except ValueError:
                print('Given number is not valid! Try again.')
                continue
            if index in range(1, len(values) + 1):
                return index

    @staticmethod
    def choose_victim(enemy_team):
        heroes = enemy_team.get_alive_heroes()

        if not enemy_team.npc:
            return Game.random_victim(heroes)

        print('Choose opponent from enemy team to attack.\n')
        for i, hero in enumerate(heroes, 1):
            print(f'{i}. {hero}')
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
    def random_victim(heroes):
        if any(hero.area == HeroAreaEnum.FRONT for hero in heroes):
            front_line = [hero for hero in heroes if hero.area == HeroAreaEnum.FRONT]
            victim = choice(front_line)
        else:
            victim = choice(heroes)
        return victim
