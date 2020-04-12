import math
import random

from displayer import print_error, print_moves, print_yellow
from models.attack import Attack
from models.enums import HeroAreaEnum
from models.game import Game


class Hero:

    def __init__(self, name: str, hp: float, defence: float,
                 speed: float, recovery: float, mind: int, img_path=None,
                 area: HeroAreaEnum = None):
        self.name = name
        self.area = area

        self.hp = hp
        self.defence = defence
        self.speed = speed
        self.recovery = recovery
        self.mind = mind

        self.initial_hp = hp
        self.initial_defence = defence
        self.initial_speed = speed

        self.moves = []
        self.alive = True
        self.stunned = 0
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

    def reset_flags(self):
        self.shield = 0
        self.stunned -= 1

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
    def calculate_damage(attack, victim_hero, damage_multiplier, defence_multiplier):
        damage = (
            (damage_multiplier * attack.power)
            - (defence_multiplier * victim_hero.defence)
            - victim_hero.shield
        )
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

    def critical_and_block_calculation(self, target):
        base_chance = 15
        damage_multiplier = defence_multiplier = 1
        self_critical_chance = max(base_chance + (self.mind - target.mind) / 2, 0)
        targets_block_chance = max(base_chance + (target.mind - self.mind) / 2, 0)

        critical_success = random.random() <= self_critical_chance / 100
        block_success = random.random() <= targets_block_chance / 100
        print(f'Chance for critical: {self_critical_chance}% , '
              f'Chance for block: {targets_block_chance}%')
        if critical_success:
            damage_multiplier = 1.5
            print('Critical hit!')
        if block_success:
            defence_multiplier = 2
            print(f'Attack has been blocked by {target.name}!')

        return damage_multiplier, defence_multiplier

    def take_action(self, target_team):

        print(
            f'{self.team.name} move [ENERGY: {self.team.energy}] - {self.name} is taking action.\n'
        )

        if self.stunned > 0:
            print(f'{self.name} is stunned and cannot move!')
            return

        move = self.choose_move()

        self.team.energy -= move.cost

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
                if move.type == 'stun':
                    success = random.random() <= round(move.speed / 100, 2)
                    print(f'Success rate: {round(move.speed, 1)}%')
                    if success:
                        victim.stunned = move.power
                        print(f'{victim.name} has been stunned for {move.power} round(s)!\n')
                        continue
                    else:
                        print('You missed!\n')
                        continue
                success = random.random() <= self.hit_chance(move, victim)
                if success:

                    dmg_multiplier, def_multiplier = self.critical_and_block_calculation(victim)
                    if victim != target_hero:
                        dmg_multiplier *= 0.75
                    damage = self.calculate_damage(move, victim, dmg_multiplier, def_multiplier)

                    if move.type == 'drain':
                        Hero.increase_hp(self, damage)

                    victim.hp_reduction(damage)
                    print(f'You hit and dealt {damage} damage points!\n')

                    if move.type == 'attack stun' and damage > 0:
                        victim.stunned = 1
                        print(f'{victim.name} has been stunned for 1 round!\n')

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

        if move.sacrifice:
            self.hp_reduction(move.sacrifice)

    def self_recovery(self):
        recovery = round(self.recovery / 100 * self.hp, 1)
        self.hp = min(self.hp + recovery, self.initial_hp)

    def __repr__(self):
        return (f'{self.name} with Hp: {self.hp}, def: {self.defence}, '
                f'speed: {self.speed}, area: {self.area}')
