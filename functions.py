from operator import attrgetter
from random import choice


def sorted_by_speed(team):
    return sorted(team, key=attrgetter('speed'), reverse=True)


def ask_victim(team):
    while True:
        try:
            print('\nChoose one of your opponents.')
            num = int(input('Number of opponent is: '))
        except ValueError:
            continue
        if num in range(1, len(team)+1):
            return num


def choose_victim(team):
    print('Choose opponent from enemy team to attack\n')
    number = 1
    for hero in range(0, len(team)):
        print(f'{number}. {team[number-1]},')
        number += 1
    num = ask_victim(team)
    if any(hero.area == 'front' for hero in team):
        while team[num-1].area != 'front':
            print(f'Cannot attack {team[num - 1].name} now.')
            print('First eliminate warriors from the front area.')
            num = ask_victim(team)
        return team[num-1]
    else:
        return team[num-1]


def random_victim(team):
    if any(hero.area == 'front' for hero in team):
        victim = choice(team)
        while victim.area != 'front':
            victim = choice(team)
        return victim
    else:
        victim = choice(team)
    return victim
