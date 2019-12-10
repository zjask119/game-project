from models import HeroAreaEnum
from functions import (
    sorted_by_speed, choose_victim, random_victim, choose_attack, damage_calc,
    dodge_chance, hp_reduction, stat_reduction, roll
)
from utils import prepare_teams


def main():
    teams = prepare_teams()
    human_team = teams[0]
    comp_team = teams[1]

    available_areas = [f'{x.value} -> {x.name} area'
                       for x in HeroAreaEnum.__members__.values()]
    print('Assign one of the listed areas to the heroes:\n',
          '\n'.join(available_areas))

    for hero in human_team.get_heroes():
        while True:
            try:
                area_num = int(input(f'Choose area (number) for hero {hero.name}: '))
                area = HeroAreaEnum(area_num)
            except ValueError:
                print('Number is not valid! Try again')
            else:
                hero.area = area
                break

    print(f'\nThe fight between: \nteam: {human_team}\nand\nteam: {comp_team}\nhas begun...')

    round = 0
    heroes = human_team.get_heroes().copy()
    enemies = comp_team.get_heroes().copy()
    heroes = sorted_by_speed(heroes)
    enemies = sorted_by_speed(enemies)

    while human_team.is_anybody_alive() and comp_team.is_anybody_alive():
        round += 1
        if human_team.energy < 8:
            human_team.energy += 2
        if comp_team.energy < 8:
            comp_team.energy += 2

        print(f'-------------------------- Round {round} --------------------------\n')

        turns = len(human_team.get_heroes()) + len(comp_team.get_heroes())

        for i in range(0, turns):
            try:
                if heroes[0].speed >= enemies[0].speed:  # player has priority if the speed is equal for both
                    player_hero = heroes[0]
                    print(f'{player_hero.name} is attacking. Energy status: {human_team.energy}')
                    victim_position = choose_victim(enemies)
                    victim = enemies[victim_position]
                    attack = choose_attack(player_hero.moves)
                    dodge = dodge_chance(attack.speed, victim.speed)
                    print(f'Success rate: {dodge * 100}%')
                    if roll(dodge):
                        print('SUCCESS!')
                        damage = damage_calc(attack.power, victim.defence)
                        victim.hp = hp_reduction(damage, victim.hp)
                        victim.speed = stat_reduction(comp_team.get_heroes()[victim_position].hp, victim.hp, victim.speed)
                        victim.defence = stat_reduction(comp_team.get_heroes()[victim_position].hp, victim.hp, victim.defence)
                        for attack in victim.moves:
                            attack.power = stat_reduction(comp_team.get_heroes()[victim_position].hp, victim.hp, attack.power)
                            attack.speed = stat_reduction(comp_team.get_heroes()[victim_position].hp, victim.hp, attack.speed)
                        print(f'{player_hero.name} attacked {victim.name} and dealt {damage} damage points.\n')
                    else:
                        print(f'FAILED! {player_hero.name} missed!')
                else:
                    npc_hero = enemies[0]
                    print(f'{npc_hero.name} is attacking.')
                    print(f'{npc_hero.name} attacked {random_victim(human_team.get_heroes()).name}\n')
            except IndexError:
                raise
            else:
                if len(enemies) == 0:
                    print(f'{heroes[0].name} is attacking.')
                    print(f'Selected move: {choose_attack(heroes[0].moves)}')
                    print(f'{heroes[0].name} attacked {choose_victim(comp_team.get_heroes()).name}')
                    break
                if len(heroes) == 0:
                    print(f'{enemies[0].name} is attacking.')
                    break


if __name__ == "__main__":
    main()
