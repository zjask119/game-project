from models import Hero, HeroAreaEnum
from functions import sorted_by_speed, choose_victim, random_victim


def main():
    team1 = [
        Hero('Batman', 200, 40, 70, 50),
        Hero('Superman', 210, 40, 80, 60),
        Hero('Green Lantern', 180, 30, 90, 90),
        Hero('Wonder Woman', 180, 30, 70, 60),
        ]

    team2 = [
        Hero('Spider-Man', 190, 40, 80, 70, HeroAreaEnum.BACK),
        Hero('Thor', 180, 30, 80, 80, HeroAreaEnum.BACK),
        Hero('Iron Man', 190, 40, 70, 60, HeroAreaEnum.FRONT),
        Hero('Hulk', 190, 40, 80, 80, HeroAreaEnum.BACK),
        ]

    area_text_list = [f'{x.value} -> {x.name} area'
                      for x in HeroAreaEnum.__members__.values()]
    print('Assign one of the listed areas to the heroes:\n',
          '\n'.join(area_text_list))

    for hero in team1:
        while True:
            try:
                area_num = int(input(f'Choose area (number) for hero {hero.name}: '))
                area = HeroAreaEnum(area_num)
            except ValueError:
                print('Number is not valid! Try again')
            else:
                hero.area = area
                break

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


if __name__ == "__main__":
    main()