import sqlite3
from random import sample

from config import DB_DIR
from displayer import print_error, print_hero_areas, print_heroes
from models.attack import Attack
from models.enums import HeroAreaEnum
from models.hero import Hero
from models.team import Team


def get_heroes_from_db():
    conn = sqlite3.connect(DB_DIR)
    cursor = conn.cursor()
    query = 'select id, name, hp, defence, speed, recovery, mind, path from Hero'
    cursor.execute(query)
    db_heroes = cursor.fetchall()

    query = '''
        select name, power, speed, cost, type, sacrifice, range, user 
        from Move
    '''
    cursor.execute(query)
    db_moves = cursor.fetchall()

    heroes = {}
    moves = []

    for db_hero in db_heroes:
        hero_id, name, hp, defence, speed, recovery, mind, img_path = db_hero
        hero = Hero(name, hp, defence, speed, recovery, img_path)
        heroes[hero_id] = hero

    for db_move in db_moves:
        name, power, speed, cost, type_, sacrifice, range_, user = db_move
        assert range_ in ('target', 'area', 'self', 'self area')
        power = power if power else 0

        move = Attack(name, power, speed, cost, sacrifice, type_, range_)
        moves.append((user, move))

    for hero_id, move in moves:
        hero = heroes[hero_id]
        if move.speed is None:
            move.speed = hero.speed
            move.initial_speed = hero.speed
        hero.add_move(move)

    return list(heroes.values())


def prepare_teams():
    team1_as_npc = False
    team1 = Team('Player 1', team1_as_npc)
    answer = ''
    while answer not in ['n', 'p']:
        answer = input('Wanna fight with NPC [n/N] or other player [p/P]? ').lower().strip()
    team2 = Team(name='Player 2' if answer == 'p' else 'CPU',
                 npc=False if answer == 'p' else True)
    print()
    return team1, team2


def random_heroes(heroes):
    while True:
        try:
            number = int(input('How many heroes would you like to draw?\n'))
        except ValueError:
            print_error('Number is not valid! Try again')
        else:
            break
    return sample(range(1, len(heroes) + 1), number)


def assign_heroes_to_team(heroes, team):
    max_heroes = 5

    while True:
        print(f'Assigning heroes to team {team.name}:')
        print_heroes(heroes)

        print('Enter a list of heroes whitespace separated [0 if random]:')
        choices = set(map(int, input().split()))

        if len(choices) == 1 and list(choices)[0] == 0:
            choices = random_heroes(heroes)
            break

        if not choices.issubset(set(range(1, len(heroes) + 1))):
            print_error('Given numbers are valid! Try again.')
            continue
        if not (0 < len(choices) <= max_heroes):
            print_error('Choose at least one hero, maximum five!')
            continue
        break

    selected_heroes = [heroes[choice - 1] for choice in choices]
    print(f'\nYou have chosen {", ".join([hero.name for hero in selected_heroes])}.\n')
    for selected_hero in selected_heroes:
        assign_hero_to_area(selected_hero)
        team.add_hero(selected_hero)
        heroes.remove(selected_hero)

    print(f'{team.name} is completed.\n')


def assign_hero_to_area(hero):
    print(f'Assign {hero.name} to one of the listed areas: ')
    print_hero_areas([x for x in HeroAreaEnum.__members__.values()])

    while True:
        try:
            area_num = int(input('Area: '))
            area = HeroAreaEnum(area_num)
        except ValueError:
            print_error('Number is not valid! Try again')
        else:
            hero.area = area
            break
