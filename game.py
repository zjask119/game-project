from models import Hero
from functions import sorted_by_speed, choose_victim, random_victim


team1 = [
    Hero('Batman', 200, 40, 70, 50, 'back'),
    Hero('Superman', 210, 40, 80, 60, 'front'),
    Hero('Green Lantern', 180, 30, 90, 90, 'back'),
    Hero('Wonder Woman', 180, 30, 70, 60, 'back'),
    ]

team2 = [
    Hero('Spider-Man', 190, 40, 80, 70, 'back'),
    Hero('Thor', 180, 30, 80, 80, 'back'),
    Hero('Iron Man', 190, 40, 70, 60, 'front'),
    Hero('Hulk', 190, 40, 80, 80, 'back'),
    ]

print(f'\nThe fight between: \nteam: {team1}\nand\nteam: {team2}\nhas begun...')

round = 0

while len(team1) > 0 and len(team2) > 0:
    round += 1
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
                print(f'{player_hero.name} attacked {choose_victim(team2).name}\n')
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
                print(f'{heroes[0].name} attacked {choose_victim(team2).name}')
                break
            if len(heroes) == 0:
                print(f'{enemies[0].name} is attacking.')
                break
