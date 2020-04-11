import math
import random

from displayer import print_error, print_moves, print_yellow
from models.attack import Attack
from models.enums import HeroAreaEnum
from models.game import Game


class Hero:

    def __init__(self, name: str, hp: float, defence: float,
                 speed: float, recovery: float, img_path=None,
                 area: HeroAreaEnum = None):
        self.name = name
        self.area = area

        self.hp = hp
        self.defence = defence
        self.speed = speed
        self.recovery = recovery

        self.initial_hp = hp
        self.initial_defence = defence
        self.initial_speed = speed

        self.moves = []
        self.alive = True
        self.stunned = False
        self.shield = 0
        self.team = None

        # GUI
        self.active = False
        self.victim = False
        self.img_path = img_path
        self.id = None

    def add_move(self, move):
        assert isinstance(move, Attack)
        move.id = len(self.moves) + 1
        self.moves.append(move)

    def reset_shield(self):
        self.shield = 0

    @property
    def reduction_factor(self):
        factor = self.hp / self.initial_hp
        return round(math.sqrt(factor), 2)

    def update_attributes(self):
        self.speed = round(self.initial_speed * self.reduction_factor, 1)
        self.defence = round(self.initial_defence * self.reduction_factor, 1)
        for move in self.moves:
            if move.type in ('attack const', 'heal'):
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

    def choose_move(self):
        if self.team.npc:
            affordable_moves = [move for move in self.moves
                                if move.cost <= self.team.energy]
            move = random.choice(affordable_moves)
        else:
            while True:
                print('Choose one of possible moves:')
                print_moves(self.moves)
                num = Game.ask_number(self.moves) - 1
                move = self.moves[num]
                if move.cost > self.team.energy:
                    print_error("Not enough energy - choose another attack!")
                    continue
                break
        return move

    @staticmethod
    def increase_hp(hero, heal):
        new_hp = min(hero.initial_hp, hero.hp + heal)
        healed_by = round(new_hp - hero.hp, 1)

        hero.hp = new_hp
        hero.update_attributes()
        print(f'{hero.name} has been healed by {healed_by} hp!')

    @staticmethod
    def heal_hero(move, hero):
        heal = (move.power / 100) * hero.initial_hp
        heal = round(heal, 1)
        Hero.increase_hp(hero, heal)

    def take_action(self, target_team):

        print(
            f'{self.team.name} move [ENERGY: {self.team.energy}] - {self.name} is taking action.\n'
        )

        if self.stunned:
            print(f'{self.name} is stunned and cannot move!')
            self.stunned = False
            return

        move = self.choose_move()

        self.team.energy -= move.cost
        if move.sacrifice:
            self.hp_reduction(move.sacrifice)

        if move.type in ('attack', 'attack const', 'stun', 'attack stun', 'drain'):
            target_hero = Game.choose_target(self.team, target_team)
            if move.range == 'area':
                victims = [hero for hero in target_hero.team.get_alive_heroes()
                           if hero.area == target_hero.area]
            elif move.range == 'target':
                victims = [target_hero]
            else:
                # TODO
                # raise NotImplementedError
                return None

            print(f'{self.name} is using {move.range} attack {move.name}.')
            for victim in victims:
                victim.victim = True
                print(f'{self.name} is attacking {victim.name}.')
                success = random.random() < self.hit_chance(move, victim)
                if success:
                    if move.type == 'stun':
                        victim.stunned = True
                        print(f'{victim.name} has been stunned!\n')
                        continue

                    if move.type == 'attack stun':
                        victim.stunned = True
                        print(f'{victim.name} has been stunned!\n')

                    damage_multiplier = 1
                    if victim != target_hero:
                        damage_multiplier = 0.75
                    damage = self.calculate_damage(move, victim, damage_multiplier)

                    if move.type == 'drain':
                        Hero.increase_hp(self, damage)

                    victim.hp_reduction(damage)
                    print(f'You hit and dealt {damage} damage points!\n')

                    if not victim.alive:
                        print_yellow(f'{victim.name} is dead!\n')

                else:
                    print('You missed!\n')

        elif move.type == 'shield':
            target_heroes = []
            if move.range == 'self':
                target_heroes = [self]
            elif move.range == 'self area':
                target_heroes = self.team.get_alive_heroes(area=self.area)

            for hero in target_heroes:
                print(f'{hero.name} got {move.power} shield.')
                hero.shield += move.power

        elif move.type == 'heal':
            if move.range == 'self':
                target_heroes = [self]
            elif move.range == 'target':
                target = Game.choose_target(self.team)
                target_heroes = [target]
            elif move.range == 'self area':
                target_heroes = self.team.get_alive_heroes(area=self.area)
            else:
                # raise NotImplementedError
                return None

            for hero in target_heroes:
                Hero.heal_hero(move, hero)
        else:
            # raise NotImplementedError
            return None

    def self_recovery(self):
        recovery = round(self.recovery / 100 * self.hp, 1)
        self.hp = min(self.hp + recovery, self.initial_hp)

    def __repr__(self):
        return (f'{self.name} with Hp: {self.hp}, def: {self.defence}, '
                f'speed: {self.speed}, area: {self.area}')
