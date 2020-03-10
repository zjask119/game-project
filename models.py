from enum import Enum
from math import sqrt
from operator import attrgetter
from random import random, choice


class HeroAreaEnum(Enum):
    FRONT = 1
    BACK = 2

    def __str__(self):
        return self.name


class Game:

    def __init__(self, teams=None):
        self.teams = []
        if teams and isinstance(teams, list):
            for team in teams:
                self.add_team(team)

    def add_team(self, team):
        assert isinstance(team, Team)
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
            while heroes[num-1].area != HeroAreaEnum.FRONT:
                print(f'Cannot attack {heroes[num - 1].name} now.')
                print('First eliminate warriors from the front area.')
                num = Game.ask_number(heroes)
            return heroes[num-1]
        else:
            return heroes[num-1]

    @staticmethod
    def random_victim(heroes):
        if any(hero.area == HeroAreaEnum.FRONT for hero in heroes):
            front_line = [hero for hero in heroes if hero.area == HeroAreaEnum.FRONT]
            victim = choice(front_line)
        else:
            victim = choice(heroes)
        return victim


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


class Hero:

    def __init__(self,  name: str, hp: float, defence: float,
                 speed: float, moves: list,
                 area: HeroAreaEnum = HeroAreaEnum.BACK):
        self.name = name
        self.current_hp = hp
        self.initial_hp = hp
        self.initial_defence = defence
        self.initial_speed = speed
        self.moves = moves
        self.area = area
        self.alive = True
        self.team = None

    @property
    def speed(self):
        return round(self.initial_speed * self.reduction_factor, 1)

    @property
    def defence(self):
        return round(self.initial_defence * self.reduction_factor, 1)

    @property
    def reduction_factor(self):
        factor = self.current_hp / self.initial_hp
        return round(sqrt(factor), 1)

    @staticmethod
    def hit_chance(attack, victim_hero):
        chance = 1
        if attack.speed < victim_hero.speed:
            chance = 1 - (((victim_hero.speed - attack.speed) * 2) / 100)
            chance = min(0.9, chance)
            chance = max(0.1, chance)
        print(f'Success rate: {chance * 100}%')
        return round(chance, 2)

    @staticmethod
    def damage_calc(attack, victim_hero):
        damage = attack.power - victim_hero.defence
        return max(0, damage)

    def hp_reduction(self, damage):
        new_hp = self.current_hp - damage
        new_hp = max(0, new_hp)
        if new_hp == 0:
            self.alive = False
        self.current_hp = new_hp
              
    def choose_attack(self):
        if self.team.npc:
            return choice(self.moves)
        while True:
            print('Choose one of possible moves.\n')
            for i, attack in enumerate(self.moves, 1):
                print(f'{i}. {attack}')
            num = Game.ask_number(self.moves)
            if self.moves[num - 1].cost <= self.team.energy:
                self.team.energy -= self.moves[num - 1].cost
                return self.moves[num - 1]
            else:
                print("LOW ENERGY!")
                continue
    
    def attack_hero(self, victim_hero):
        attack = self.choose_attack()
        success = random() < self.hit_chance(attack, victim_hero)
        if not success:
            print('You missed, looser')
            return

        damage = self.damage_calc(attack, victim_hero)
        print(f'{self.name} attacked {victim_hero.name} and dealt {damage} damage points.\n')
        victim_hero.hp_reduction(damage)

    def __repr__(self):
        return f'{self.name} with Hp: {self.current_hp}, def: {self.defence}, speed: {self.speed}, area: {self.area}'


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

