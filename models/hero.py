import math
import random

from displayer import print_error, print_moves
from models.attack import Attack
from models.enums import HeroAreaEnum
from models.game import Game


class Hero:

    def __init__(self, name: str, hp: float, defence: float,
                 speed: float, area: HeroAreaEnum = None):
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
        self.hp = round(new_hp, 0)

    def choose_move(self):
        if self.team.npc:
            affordable_moves = [move for move in self.moves
                                if move.cost <= self.team.energy]
            move = random.choice(affordable_moves)
            return move
        else:
            while True:
                print('Choose one of possible moves:')
                print_moves(self.moves)
                num = Game.ask_number(self.moves) - 1
                move = self.moves[num]
                if move.cost > self.team.energy:
                    print_error("Not enough energy - choose another attack!")
                    continue
                return move

    def take_action(self, victim_hero):
        move = self.choose_move()

        self.team.energy -= move.cost
        if move.sacrifice:
            self.hp_reduction(move.sacrifice)

        if move.type in ('attack', 'attack const', 'stun'):
            if move.range == 'area':
                victims = [hero for hero in victim_hero.team.get_alive_heroes()
                           if hero.area == victim_hero.area]
            elif move.range == 'target':
                victims = [victim_hero]
            else:
                raise NotImplementedError

            print(f'{self.name} is using {move.range} attack {move.name}.')
            for victim in victims:
                print(f'{self.name} is attacking {victim.name}.')
                success = random.random() < self.hit_chance(move, victim)
                if success:
                    if move.type == 'stun':
                        victim.stunned = True
                        print(f'{victim.name} has been stunned!')
                        continue
                    damage_multiplier = 1
                    if victim != victim_hero:
                        damage_multiplier = 0.75
                    damage = self.calculate_damage(move, victim, damage_multiplier)
                    victim.hp_reduction(damage)
                    print(f'You hit and dealt {damage} damage points!\n')
                else:
                    print('You missed!\n')

        elif move.type == 'shield':
            target_heroes = []
            if move.range == 'target':
                target_heroes = [self]
            elif move.range == 'self area':
                target_heroes = self.team.get_alive_heroes(area=self.area)

            for hero in target_heroes:
                print(f'{hero} got {move.power} shield.')
                hero.shield += move.power

        elif move.type == 'heal':
            if move.range == 'self':
                heal = (move.power / 100) * self.initial_hp
                heal = round(heal, 0)
                new_hp = min(self.initial_hp, self.hp + heal)
                healed_by = new_hp - self.hp

                self.hp = new_hp
                print(f'{self.name} has been healed by {healed_by} hp')
            elif move.range == 'target':
                raise NotImplementedError

        else:
            raise NotImplementedError

    def __repr__(self):
        return (f'{self.name} with Hp: {self.hp}, def: {self.defence}, '
                f'speed: {self.speed}, area: {self.area}')
