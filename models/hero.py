import math
import random

from models.enums import HeroAreaEnum
from models.game import Game


class Hero:

    def __init__(self, name: str, hp: float, defence: float,
                 speed: float, moves: list,
                 area: HeroAreaEnum = HeroAreaEnum.BACK):
        self.name = name

        self.hp = hp
        self.defence = defence
        self.speed = speed

        self.initial_hp = hp
        self.initial_defence = defence
        self.initial_speed = speed

        self.moves = moves
        self.area = area
        self.alive = True
        self.team = None

    @property
    def reduction_factor(self):
        factor = self.hp / self.initial_hp
        return round(math.sqrt(factor), 1)

    def reduce_attributes(self):
        self.speed = round(self.initial_speed * self.reduction_factor, 1)
        self.defence = round(self.initial_defence * self.reduction_factor, 1)
        for move in self.moves:
            move.power = round(move.power * self.reduction_factor, 1)
            move.speed = round(move.speed * self.reduction_factor, 1)

    @staticmethod
    def hit_chance(attack, victim_hero):
        chance = 1
        if attack.speed < victim_hero.speed:
            chance = 1 - round((((victim_hero.speed - attack.speed) * 2) / 100), 1)
            chance = min(0.9, chance)
            chance = max(0.1, chance)
        print(f'Success rate: {chance * 100}%')
        return round(chance, 2)

    @staticmethod
    def damage_calc(attack, victim_hero):
        damage = round(attack.power - victim_hero.defence, 1)
        return max(0, damage)

    def hp_reduction(self, damage):
        new_hp = self.hp - damage
        new_hp = max(0, new_hp)
        if new_hp == 0:
            self.alive = False
        self.hp = round(new_hp, 1)

    def choose_attack(self):
        if self.team.npc:
            return random.choice(self.moves)
        while True:
            print('Choose one of possible moves.\n')
            for i, attack in enumerate(self.moves, 1):
                print(f'{i}. {attack}')
            num = Game.ask_number(self.moves) - 1
            move = self.moves[num]

            if move.cost <= self.team.energy:
                self.team.energy -= move.cost
                return move
            else:
                print("LOW ENERGY! - Choose another attack")
                continue

    def attack_hero(self, victim_hero):
        attack = self.choose_attack()
        success = random.random() < self.hit_chance(attack, victim_hero)
        if not success:
            print('You missed, looser')
            return

        damage = self.damage_calc(attack, victim_hero)
        print(
            f'{self.name} attacked {victim_hero.name} and dealt {damage} damage points.\n')
        victim_hero.hp_reduction(damage)

    def __repr__(self):
        return f'{self.name} with Hp: {self.hp}, def: {self.defence}, speed: {self.speed}, area: {self.area}'
