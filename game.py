from models import HeroAreaEnum
from functions import (
    choose_victim, random_victim, choose_attack, damage_calc,
    dodge_chance, hp_reduction, stat_reduction, roll
)
from utils import prepare_teams


def main():
    human_team, comp_team = prepare_teams()

    available_areas = [f'{x.value} -> {x.name} area'
                       for x in HeroAreaEnum.__members__.values()]
    print('Assign one of the listed areas to the heroes:\n',
          '\n'.join(available_areas))

    for hero in human_team.get_all_heroes():
        while True:
            try:
                area_num = int(input(f'Choose area (number) for hero {hero.name}: '))
                area = HeroAreaEnum(area_num)
            except ValueError:
                print('Number is not valid! Try again')
            else:
                hero.area = area
                break

    print(f'\nThe fight between:\n'
          f'{human_team}\n'
          f'and\n'
          f'{comp_team}\n'
          f'has begun...')

    game_round = 0

    while human_team.is_anybody_alive() and comp_team.is_anybody_alive():

        human_heroes = human_team.get_alive_heroes(sorted_by='speed')
        comp_heroes = comp_team.get_alive_heroes(sorted_by='speed')

        game_round += 1
        if human_team.energy < 8:
            human_team.energy += 2
        if comp_team.energy < 8:
            comp_team.energy += 2

        print(f'-------------------------- Round {game_round} --------------------------\n')

        turns = human_team.num_of_alive_heroes + comp_team.num_of_alive_heroes

        for i in range(0, turns):
            try:
                if human_heroes[0].speed >= comp_heroes[0].speed:  # player has priority if the speed is equal for both
                    player_hero = human_heroes[0]
                    print(f'{player_hero.name} is attacking. Energy status: {human_team.energy}')
                    victim_position = choose_victim(comp_heroes)
                    victim = comp_heroes[victim_position]
                    attack = choose_attack(player_hero.moves)
                    dodge = dodge_chance(attack.speed, victim.speed)
                    print(f'Success rate: {dodge * 100}%')
                    if roll(dodge):
                        print('SUCCESS!')
                        damage = damage_calc(attack.power, victim.defence)
                        victim.hp = hp_reduction(damage, victim.hp)
                        victim.speed = stat_reduction(comp_heroes[victim_position].hp, victim.hp, victim.speed)
                        victim.defence = stat_reduction(comp_heroes[victim_position].hp, victim.hp, victim.defence)
                        for attack in victim.moves:
                            attack.power = stat_reduction(comp_heroes[victim_position].hp, victim.hp, attack.power)
                            attack.speed = stat_reduction(comp_heroes[victim_position].hp, victim.hp, attack.speed)
                        print(f'{player_hero.name} attacked {victim.name} and dealt {damage} damage points.\n')
                    else:
                        print(f'FAILED! {player_hero.name} missed!')
                else:
                    npc_hero = comp_heroes[0]
                    print(f'{npc_hero.name} is attacking.')
                    print(f'{npc_hero.name} attacked {random_victim(human_heroes).name}\n')
            except IndexError:
                raise
            else:
                if len(comp_heroes) == 0:
                    print(f'{human_heroes[0].name} is attacking.')
                    print(f'Selected move: {choose_attack(human_heroes[0].moves)}')
                    print(f'{human_heroes[0].name} attacked {choose_victim(comp_heroes).name}')
                    break
                if len(human_heroes) == 0:
                    print(f'{comp_heroes[0].name} is attacking.')
                    break


if __name__ == "__main__":
    main()
