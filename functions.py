from operator import attrgetter
from random import choice

from models import HeroAreaEnum


def sorted_by_speed(team):
    return sorted(team, key=attrgetter('speed'), reverse=True)


def ask_victim(team):
    while True:
        try:
            print(f'\nChoose one of your opponents (1 - {len(team)}).')
            index = int(input('Number of opponent is: '))
        except ValueError:
            print('Given number is not valid! Try again.')
            continue
        if index in range(1, len(team)+1):
            return index


def choose_victim(team, team_energy):
    print('Choose opponent from enemy team to attack.\n')
    print(f'Energy status: {team_energy}')
    for i, hero in enumerate(team, 1):
        print(f'{i}. {hero}')
    num = ask_victim(team)
    if any(hero.area == HeroAreaEnum.FRONT for hero in team):
        while team[num-1].area != HeroAreaEnum.FRONT:
            print(f'Cannot attack {team[num - 1].name} now.')
            print('First eliminate warriors from the front area.')
            num = ask_victim(team)
        return team[num-1]
    else:
        return team[num-1]


def random_victim(team):
    if any(hero.area == HeroAreaEnum.FRONT for hero in team):
        front_line = [hero for hero in team if hero.area == HeroAreaEnum.FRONT]
        victim = choice(front_line)
        return victim
    else:
        victim = choice(team)
    return victim
