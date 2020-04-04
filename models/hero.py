import math
import random

from displayer import print_moves
from models.attack import Attack
from models.enums import HeroAreaEnum
from models.game import Game


class Hero:

    def __init__(self, name: str, hp: float, defence: float,
                 speed: float, area: HeroAreaEnum = HeroAreaEnum.BACK):
        self.name = name
        self.area = area

        self.hp = hp
        self.defence = defence
        self.speed = speed

        self.initial_hp = hp
        self.initial_defence = defence
        self.initial_speed = speed

        self.moves = []
        self.alive = True
        self.stunned = False
        self.shield = 0
        self.team = None

    def add_move(self, move):
        assert isinstance(move, Attack)
        self.moves.append(move)

    def reset_shield(self):
        self.shield = 0

    @property
    def reduction_factor(self):
        factor = self.hp / self.initial_hp
        return round(math.sqrt(factor), 2)

    def reduce_attributes(self):
        self.speed = round(self.initial_speed * self.reduction_factor, 1)
        self.defence = round(self.initial_defence * self.reduction_factor, 1)
        for move in self.moves:
            if move.type == 'constant':
                continue
            move.power = round(move.initial_power * self.reduction_factor, 1)
            move.speed = round(move.initial_speed * self.reduction_factor, 1)

    @staticmethod
    def hit_chance(attack, victim_hero):
        div = attack.speed / victim_hero.speed
        if div <= 0.5:
            chance = 0
        elif 0.5 < div < 2:
            chance = 0.5 * math.log(2 * div, 2)
        else:
            chance = 1

        chance = max(0.05, chance)
        chance = min(0.95, chance)
        chance = round(chance, 2)

        print(f'Success rate: {round(chance * 100, 1)}%')
        return chance

    @staticmethod
    def calculate_damage(attack, victim_hero, damage_multiplier=1):
        damage = damage_multiplier * attack.power - victim_hero.defence - victim_hero.shield
        damage = round(damage, 1)
        return max(0, damage)

    def hp_reduction(self, damage):
        new_hp = self.hp - damage
        new_hp = max(0, new_hp)
        if new_hp == 0:
            self.alive = False
        self.hp = round(new_hp, 1)

    def choose_attack(self):
        if self.team.npc:
            affordable_moves = [move for move in self.moves
                                if move.cost <= self.team.energy]
            move = random.choice(affordable_moves)
            return move
        else:
            while True:
                print('Choose one of possible moves.\n')
                print_moves(self.moves)
                num = Game.ask_number(self.moves) - 1
                move = self.moves[num]
                if move.cost > self.team.energy:
                    print("LOW ENERGY! - Choose another attack")
                    continue
                return move

    def take_action(self, victim_hero):
        attack = self.choose_attack()

        self.team.energy -= attack.cost
        if attack.sacrifice:
            self.hp_reduction(attack.sacrifice)

        if attack.range == 'area':
            victims = [hero for hero in victim_hero.team.get_alive_heroes()
                       if hero.area == victim_hero.area]
        elif attack.range == 'target':
            victims = [victim_hero]
        elif attack.range == 'self':
            victims = []
            if attack.type == 'shield':
                self.shield += attack.power
                print(f'shield: {self.shield}')
        else:
            raise NotImplementedError

        print(f'{self.name} is using {attack.range} move {attack.name}.')
        for victim in victims:
            success = random.random() < self.hit_chance(attack, victim)
            print(f'{self.name} is attacking {victim.name}.')
            if success:
                if attack.type == 'stun':
                    victim.stunned = True
                    continue
                damage_multiplier = 1
                if victim != victim_hero:
                    damage_multiplier = 0.75
                damage = self.calculate_damage(attack, victim, damage_multiplier)
                print(f'You hit and dealt {damage} damage points!\n')
                victim.hp_reduction(damage)
            else:
                print('You missed!\n')

    def __repr__(self):
        return (f'{self.name} with Hp: {self.hp}, def: {self.defence}, '
                f'speed: {self.speed}, area: {self.area}')
