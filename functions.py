from operator import attrgetter
from random import choice, random
from math import sqrt

from models import HeroAreaEnum


def sorted_by_speed(team):
    return sorted(team, key=attrgetter('speed'), reverse=True)


def ask_values(values):
    while True:
        try:
            print(f'\nChoose between 1 - {len(values)}.')
            index = int(input('Your Choice is: '))
        except ValueError:
            print('Given number is not valid! Try again.')
            continue
        if index in range(1, len(values) + 1):
            return index


def choose_victim(team):
    print('Choose opponent from enemy team to attack.\n')
    for i, hero in enumerate(team, 1):
        print(f'{i}. {hero}')
    num = ask_values(team)
    if any(hero.area == HeroAreaEnum.FRONT for hero in team):
        while team[num-1].area != HeroAreaEnum.FRONT:
            print(f'Cannot attack {team[num - 1].name} now.')
            print('First eliminate warriors from the front area.')
            num = ask_values(team)
        return num-1
    else:
        return num-1


def choose_attack(attacks):
    print('Choose one of possible moves.\n')
    for i, attack in enumerate(attacks, 1):
        print(f'{i}. {attack}')
    num = ask_values(attacks)
    return attacks[num-1]


def random_victim(team):
    if any(hero.area == HeroAreaEnum.FRONT for hero in team):
        front_line = [hero for hero in team if hero.area == HeroAreaEnum.FRONT]
        victim = choice(front_line)
        return victim
    else:
        victim = choice(team)
    return victim


def dodge_chance(attack_speed, victim_speed):
    chance = ((victim_speed - attack_speed) * 2) / 100
    if attack_speed < victim_speed:
        if chance < 0.1:
            return 0.1
        if chance > 0.9:
            return 0.9
        else:
            return float(chance)
    else:
        return 1.0


def roll(chance):
    if random() < chance:
        return True
    else:
        return False


def damage_calc(attack, defence):
    damage = attack - defence
    if damage > 0:
        return damage
    else:
        return 0


def hp_reduction(damage, victim_hp):
    if victim_hp > damage:
        victim_hp -= damage
        if victim_hp > 1:
            return victim_hp
        else:
            return 1
    else:
        return 1


def stat_reduction(prev_hp, present_hp, stat):
    factor = present_hp / prev_hp
    factor = sqrt(factor)
    stat = stat * factor
    return round(stat, 1)
