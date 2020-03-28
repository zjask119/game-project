import sqlite3

from displayer import print_error
from models.attack import Attack
from models.enums import HeroAreaEnum
from models.hero import Hero
from models.team import Team


def get_heroes_from_db():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    query = 'select id, name, hp, defence, speed from hero;'
    cursor.execute(query)
    db_heroes = cursor.fetchall()

    query = 'select name, power, speed, cost, constant, user from move;'
    cursor.execute(query)
    db_moves = cursor.fetchall()

    heroes = {}
    moves = []

    for db_hero in db_heroes:
        hero_id, name, hp, defence, speed = db_hero
        hero = Hero(name, hp, defence, speed)
        heroes[hero_id] = hero

    for db_move in db_moves:
        name, power, speed, cost, constant, user = db_move
        cost = cost if cost else 0
        move = Attack(name, power, speed, cost)
        moves.append((user, move))

    for hero_id, move in moves:
        hero = heroes[hero_id]
        if move.speed is None:
            move.speed = hero.speed
        hero.add_move(move)

    return list(heroes.values())


def prepare_teams():
    team1 = Team('Player 1', False)
    answer = ''
    while answer not in ['n', 'p']:
        answer = input('Wanna fight with NPC [n/N] or other player [p/P] ?').lower().strip()
    team2 = Team(name='Player 2' if answer == 'p' else 'CPU',
                 npc=False if answer == 'p' else True)

    return team1, team2


def assign_heroes_to_team(heroes, team):
    while True:
        print(f'Assigning heroes to {team.name}: ')
        for x, hero in enumerate(heroes, 1):
            print(x, hero)

        print('Enter a list of heroes whitespace separated')
        choices = set(map(int, input().split()))

        if not choices.issubset(set(range(1, len(heroes) + 1))):
            print_error('Given numbers are valid! Try again.')
            continue
        if not (0 < len(choices) <= 4):
            print_error('Choose at least one hero, maximum four')
            continue
        break

    selected_heroes = [heroes[choice - 1] for choice in choices]
    for selected_hero in selected_heroes:
        assign_hero_to_area(selected_hero)
        team.add_hero(selected_hero)
        heroes.remove(selected_hero)

    print(f'{team.name} is completed.\n')


def assign_hero_to_area(hero):
    available_areas = [f'{x.value} -> {x.name} area'
                       for x in HeroAreaEnum.__members__.values()]
    print('Assign one of the listed areas to the heroes:\n',
          '\n'.join(available_areas))

    while True:
        try:
            area_num = int(input(f'Assign {hero.name} to one of the listed areas: '))
            area = HeroAreaEnum(area_num)
        except ValueError:
            print_error('Number is not valid! Try again')
        else:
            hero.area = area
            break
