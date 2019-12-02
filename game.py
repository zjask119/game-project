from models import Hero
from functions import sorted_by_speed, choose_victim, random_victim


team1 = [
    Hero('Batman', 200, 40, 70, 50, ''),
    Hero('Superman', 210, 40, 80, 60, ''),
    Hero('Green Lantern', 180, 30, 90, 90, ''),
    Hero('Wonder Woman', 180, 30, 70, 60, ''),
    ]

team2 = [
    Hero('Spider-Man', 190, 40, 80, 70, 'back'),
    Hero('Thor', 180, 30, 80, 80, 'back'),
    Hero('Iron Man', 190, 40, 70, 60, 'front'),
    Hero('Hulk', 190, 40, 80, 80, 'back'),
    ]


for hero in team1:
    hero.area = input(f'Choose "back" or "front" area for {hero.name}:')
    while not (hero.area == 'front' or hero.area == 'back'):
        print('You have to choose only between "back" and "front".')
        hero.area = input(f'\nChoose "back" or "front" area for {hero.name}:')
    print(hero)

print(f'\nThe fight between: \nteam: {team1}\nand\nteam: {team2}\nhas begun...')

round = 0
team1_energy = 0
team2_energy = 0

while len(team1) > 0 and len(team2) > 0:
    round += 1
    if team1_energy < 8:
        team1_energy += 2
    if team2_energy < 8:
        team2_energy += 2
    print(f'-------------------------- Round {round} --------------------------\n')
    player_hero = None
    npc_hero = None
    team1 = sorted_by_speed(team1)
    team2 = sorted_by_speed(team2)
    turns = len(team1) + len(team2)
    heroes = team1.copy()
    enemies = team2.copy()

    for i in range(0, turns):
        try:
            if heroes[0].speed >= enemies[0].speed:  # gracz ma pierwszeństwo nad npc jesli mają równą szybkość
                player_hero = heroes[0]
                print(f'{player_hero.name} is attacking.')
                print(f'{player_hero.name} attacked {choose_victim(team2, team1_energy).name}\n')
                heroes.remove(player_hero)
            else:
                npc_hero = enemies[0]
                print(f'{npc_hero.name} is attacking.')
                print(f'{npc_hero.name} attacked {random_victim(team1).name}\n')
                enemies.remove(npc_hero)
        except IndexError:
            continue
        else:
            if len(enemies) == 0:
                print(f'{heroes[0].name} is attacking.')
                print(f'{heroes[0].name} attacked {choose_victim(team2, team1_energy).name}')
                break
            if len(heroes) == 0:
                print(f'{enemies[0].name} is attacking.')
                break
