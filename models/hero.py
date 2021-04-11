import math
import random

from displayer import print_error, print_moves, print_yellow
from models.attack import Attack
from models.enums import HeroAreaEnum
from models.game import Game


class Hero:

    def __init__(self, name: str, hp: float, defence: float,
                 speed: float, recovery: float, mind: int, race: str,
                 nature: int, movement: int, sense: int, solar: int,
                 img_path=None, area: HeroAreaEnum = None):
        self.name = name
        self.area = area

        self.hp = hp
        self.defence = defence
        self.speed = speed
        self.recovery = recovery
        self.race = race
        self.mind = mind
        self.nature = nature
        self.movement = movement
        self.sense = sense
        self.solar = solar

        self.initial_hp = hp
        self.initial_defence = defence
        self.initial_speed = speed

        self.moves = []
        self.alive = True
        self.stunned = 0
        self.shield = 0
        self.team = None
        self.postponed_move = []

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
        if self.race != 'android':
            self.speed = round(self.initial_speed * self.reduction_factor, 1)
            self.defence = round(self.initial_defence * self.reduction_factor, 1)
            for move in self.moves:
                if move.type in ('attack const', 'heal', 'stun') or move.name == 'Spirit Bomb':
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

        chance = max(0.03, chance)
        chance = min(0.97, chance)
        chance = round(chance, 2)

        if victim_hero.name in ('Guldo', 'Hit'):
            chance = chance**3

        if victim_hero.movement == 2:
            chance = chance - 0.1
            chance = max(0.01, chance)
            print(f'{victim_hero.name} can teleport!')

        return chance

    @property
    def overall(self):
        move = self.moves[0]
        if move.type == 'attack' and move.name != 'Sword Attack':
            power = move.power
        else:
            power = self.defence
        overall = self.hp + self.defence + self.speed + power
        return int(overall / 3)

    @staticmethod
    def calc_standard_damage(attacker, victim_hero, attack, damage_multiplier, defence_multiplier):
        if attack.power > 2 * victim_hero.defence and not victim_hero.shield:
            damage = victim_hero.hp + victim_hero.defence
            return round(damage, 1)
        else:
            level_difference = victim_hero.overall / attacker.overall
            if level_difference >= 2:
                return 0
            modifier = 2 - level_difference
            modifier = modifier ** 3
            if modifier < 1:
                modifier = 1
            damage = (
                (damage_multiplier * 1.35 * attack.power)
                - (defence_multiplier * victim_hero.defence)
                - victim_hero.shield
            )
            if damage > 0:
                damage = damage / 3 * modifier
                return round(damage, 1)
            else:
                return 0

    @staticmethod
    def calculate_damage(attack, victim_hero, damage_multiplier, defence_multiplier):
        if attack.power > 2 * victim_hero.defence and not victim_hero.shield:
            damage = victim_hero.hp + victim_hero.defence
        else:
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

        if target.stunned > 0:
            critical_success = True
            block_success = False
            print(f'{target.name} is stunned and cannot block!')
        else:
            critical_success = random.random() <= self_critical_chance / 100
            block_success = random.random() <= targets_block_chance / 100
            print(f'Chance for critical: {self_critical_chance}% , '
                  f'Chance for block: {targets_block_chance}%')
        if critical_success:
            damage_multiplier = 1.25
            print('Critical hit!')
        if block_success:
            defence_multiplier = 1.5
            print(f'Attack has been blocked by {target.name}!')

        return damage_multiplier, defence_multiplier

    def body_change_calc(self, victim):
        level_difference = victim.initial_hp / self.initial_hp * 0.25

        self.initial_hp = victim.initial_hp * 0.3
        self.hp = victim.hp * 0.3
        self.initial_defence = victim.initial_defence * 0.25
        self.initial_speed = victim.initial_speed * 0.25

        for move in self.moves:
            if move.type in (
                    'attack const', 'heal', 'stun') or move.name == 'Spirit Bomb':
                continue
            move.initial_power *= level_difference
            move.initial_speed *= level_difference

    def take_action(self, target_team):

        print(
            f'{self.team.name} move [ENERGY: {self.team.energy}] - {self.name} ( {self.overall} ) is taking action.\n'
        )

        if self.stunned > 0:
            print(f'{self.name} is stunned and cannot move!')
            return

        if len(self.postponed_move) > 0:
            move = self.postponed_move[0]
            del self.postponed_move[0]

        else:
            move = self.choose_move()
            if move.name in ('Spirit Bomb', 'Special Beam Cannon', 'Final Flash', 'Fighting Bomber'):
                self.postponed_move.append(move)
                print(f'{self.name} is charging energy!')
                return

        self.team.energy -= move.cost

        if move.type in ('attack', 'attack const', 'energy', 'stun', 'attack stun', 'drain'):
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
                print(f'{self.name} ( {self.overall} ) is attacking {victim.name} ( {victim.overall} )')
                android_list = ['Evil Containment Wave',
                                'Telekinesis',
                                'Magic Touch',
                                'Stripping',
                                'Bad Breath',
                                'Hypnosis',
                                'Devilmite Beam',
                                'Body Change'
                                ]

                if move.name in android_list and victim.race == 'android':
                    print(f'It has no effect on {victim.name}!')
                    continue

                if move.name == 'Devilmite Beam' and victim.nature == 'Pure':
                    print(f'It has no effect on {victim.name}!')
                    continue

                if move.name == 'Body Change':
                    self.body_change_calc(victim)
                    victim.body_change_calc(victim)
                    victim.hp *= 0.2
                    img_list = []
                    img_list.append(self.img_path)
                    img_list.append(victim.img_path)
                    victim.img_path = img_list[0]
                    self.img_path = img_list[1]
                    print(f'They changed their bodies!')
                    self.update_attributes()
                    victim.update_attributes()
                    continue

                if move.type == 'energy' and victim.name in ('Mr. Popo') and move.power <= victim.defence * 1.5:
                    print(f'It has no effect on {victim.name}!')
                    continue

                if move.type == 'stun':
                    success = random.random() <= round(move.speed / 100, 2)
                    print(f'Success rate: {round(move.speed, 1)}%')
                    if success:
                        if move.name == 'Evil Containment Wave':
                            if victim.name != 'Piccolo':
                                victim.initial_hp *= 0.2
                                victim.hp *= 0.2
                                print(f'{victim.name} has been trapped!\n')
                                victim.stunned = move.power
                            else:
                                self.stunned = move.power
                                print('Piccolo used Evil Containment Wave Reflection!')
                                print(
                                    f'{self.name} has been trapped!\n')
                        else:
                            print(f'{victim.name} has been stunned for {move.power} round(s)!\n')
                            victim.stunned = move.power
                        continue
                    else:
                        print(f'It has no effect on {victim.name}!')
                        continue

                if move.type == 'attack stun' and move.speed > victim.defence:
                    victim.stunned = move.power
                    print(f'{victim.name} has been stunned for {move.power} round(s)!\n')
                    continue

                if victim.stunned > 0:
                    success = True

                else:
                    if victim.movement > self.movement:
                        accuracy = self.hit_chance(move, victim) - 0.03
                        print(f'{victim.name} has better movement!')
                    else:
                        accuracy = self.hit_chance(move, victim)
                        print(f'NOT BETTER MOVEMENT!')

                    if self.sense > victim.sense:
                        accuracy += 0.05
                        print(f'{victim.name} can sense Ki!')

                    if victim.solar == 1:
                        if self.sense in (0, 1):
                            accuracy -= 0.25

                    print(f'Success rate: {round(accuracy * 100, 1)}%')
                    success = random.random() <= accuracy

                if success:
                    if move.name in ('Destructo Disc', 'Death Saucer'):
                        dmg_multiplier = 1.25
                        def_multiplier = 1
                    else:
                        dmg_multiplier, def_multiplier = self.critical_and_block_calculation(victim)

                    if victim != target_hero:
                        dmg_multiplier *= 0.8
                    if move.type == 'attack':
                        damage = self.calc_standard_damage(
                            self, victim, move, dmg_multiplier, def_multiplier)
                        print(f'{damage}!!!')
                    else:
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

                elif success is False and victim.solar == 1:
                    victim.solar = 0
                    print(f'SOLAR FLARE!')
                    if self.sense in (2, 3):
                        self.stunned = 1
                    else:
                        self.stunned = 2
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

        elif move.type == 'revive':
            target = Game.choose_dead_hero(self.team)
            if target.race == 'android' and move.name != 'Rebuild':
                print(f'Cannot revive {target.name}!')
            else:
                target.alive = True
                Hero.heal_hero(move, target)

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
                if hero.race != 'android':
                    if move.name != 'Repair':
                        Hero.heal_hero(move, hero)
                    else:
                        print(f'Repairing has no effect on {hero.name}!')
                elif hero.race == 'android':
                    if move.name == 'Repair':
                        Hero.heal_hero(move, hero)
                    else:
                        print(f'Healing has no effect on {hero.name}!')
                else:
                    print(f'It has no effect on {hero.name}!')
        else:
            # raise NotImplementedError
            return None



        if move.sacrifice:
            sacrifice = move.sacrifice * 0.01
            sacrifice *= self.hp
            self.hp_reduction(sacrifice)

    def self_recovery(self):
        recovery = round(self.recovery / 100 * self.hp, 1)
        self.hp = min(self.hp + recovery, self.initial_hp)

    def __repr__(self):
        return (f'{self.name} with Hp: {self.hp}, def: {self.defence}, '
                f'speed: {self.speed}, area: {self.area}')
