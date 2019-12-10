from models import Hero, Attack, HeroAreaEnum
from functions import sorted_by_speed, \
    choose_victim, \
    random_victim, \
    choose_attack, \
    damage_calc, \
    dodge_chance, \
    hp_reduction, \
    stat_reduction, \
    roll


def main():
    team1 = [
        Hero(5, 'Batman', 200, 40, 70, [Attack(1, 'punch', 51, 70),
                                        Attack(2, 'kick', 57, 72, 1),
                                        Attack(3, 'combo', 62, 75, 2)], ),
        Hero(6, 'Superman', 210, 40, 80, [Attack(4, 'punch', 78, 80),
                                          Attack(5, 'kick', 82, 82, 1),
                                          Attack(6, 'combo', 99, 85, 2)], ),
        Hero(7, 'Green Lantern', 180, 30, 90, [Attack(7, 'punch', 80, 70),
                                               Attack(8, 'kick', 84, 70, 1),
                                               Attack(9, 'combo', 300, 70, 2)], ),
        Hero(8, 'Wonder Woman', 180, 30, 70, [Attack(10, 'punch', 71, 76),
                                              Attack(11, 'kick', 74, 77, 1),
                                              Attack(12, 'combo', 78, 79, 2)], ),
        ]

    team2 = [
        Hero(1, 'Spider-Man', 190, 40, 80, [Attack(1, 'punch', 59, 80),
                                            Attack(2, 'kick', 65, 82, 1),
                                            Attack(3, 'combo', 69, 85, 2)], HeroAreaEnum.BACK),
        Hero(2, 'Thor', 180, 30, 80, [Attack(1, 'punch', 53, 80),
                                      Attack(2, 'kick', 57, 83, 1),
                                      Attack(3, 'combo', 60, 84, 2)], HeroAreaEnum.BACK),
        Hero(3, 'Iron Man', 190, 40, 80, [Attack(1, 'punch', 51, 70),
                                          Attack(2, 'kick', 57, 72, 1),
                                          Attack(3, 'combo', 63, 77, 2)], HeroAreaEnum.FRONT),
        Hero(4, 'Hulk', 190, 40, 80, [Attack(1, 'punch', 65, 77),
                                      Attack(2, 'kick', 70, 83, 1),
                                      Attack(3, 'combo', 74, 90, 2)], HeroAreaEnum.BACK),
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
    heroes = team1.copy()
    enemies = team2.copy()
    heroes = sorted_by_speed(heroes)
    enemies = sorted_by_speed(enemies)

    # while any(hero.alive == True for hero in heroes) and (hero.alive == True for hero in enemies):
    #     pass

    while len(team1) > 0 and len(team2) > 0:
        round += 1
        if team1_energy < 8:
            team1_energy += 2
        if team2_energy < 8:
            team2_energy += 2

        print(f'-------------------------- Round {round} --------------------------\n')

        turns = len(team1) + len(team2)

        for i in range(0, turns):
            try:
                if heroes[0].speed >= enemies[0].speed:  # player has priority if the speed is equal for both
                    player_hero = heroes[0]
                    print(f'{player_hero.name} is attacking. Energy status: {team1_energy}')
                    victim_position = choose_victim(enemies)
                    victim = enemies[victim_position]
                    attack = choose_attack(player_hero.moves)
                    dodge = dodge_chance(attack.speed, victim.speed)
                    print(f'Success rate: {dodge * 100}%')
                    if roll(dodge):
                        print('SUCCESS!')
                        damage = damage_calc(attack.power, victim.defence)
                        victim.hp = hp_reduction(damage, victim.hp)
                        victim.speed = stat_reduction(team2[victim_position].hp, victim.hp, victim.speed)
                        victim.defence = stat_reduction(team2[victim_position].hp, victim.hp, victim.defence)
                        for attack in victim.moves:
                            attack.power = stat_reduction(team2[victim_position].hp, victim.hp, attack.power)
                            attack.speed = stat_reduction(team2[victim_position].hp, victim.hp, attack.speed)
                        print(f'{player_hero.name} attacked {victim.name} and dealt {damage} damage points.\n')
                    else:
                        print(f'FAILED! {player_hero.name} missed!')
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
                    print(f'Selected move: {choose_attack(heroes[0].moves)}')
                    print(f'{heroes[0].name} attacked {choose_victim(team2).name}')
                    break
                if len(heroes) == 0:
                    print(f'{enemies[0].name} is attacking.')
                    break


if __name__ == "__main__":
    main()

    while any(hero.alive == True for hero in heroes):
        pass
