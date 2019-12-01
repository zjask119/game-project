from hero import Hero
from random import shuffle
from random import choice

team1 = [
    Hero(130, 50, 130, 'Witkur'),
    Hero(200, 120, 200, 'Marcin'),
    Hero(200, 20, 120, 'Ania'),
]

team2 = [
    Hero(110, 40, 200, 'Zbyszek'),
    Hero(90, 50, 240, 'Biskup'),
    Hero(130, 70, 200, 'Sztefan'),
]


print()
for fight_round in range(1, 100):

    shuffle(team1)
    shuffle(team2)

    if len(team1) > 0 and len(team2) > 0:
        print(f'-------------------------- Round {fight_round} --------------------------\n')

        attacking_hero1 = None
        attacking_hero2 = None

        for i in range(len(team1) + len(team2)):
            try:
                attacking_hero1 = team1[i]
                attacking_hero2 = team2[i]
            except IndexError:
                continue

            print(f'{attacking_hero1.name} is attacking.')
            print('--------------------------')

            victim2 = choice(team2)
            damage = attacking_hero1.make_attack()
            victim2.get_hit(damage)
            if victim2.is_dead:
                team2.remove(victim2)
                print()
            else:
                print(victim2, '\n')

            print(f'{attacking_hero2.name} is attacking.')
            print('--------------------------')

            victim1 = choice(team1)
            damage = attacking_hero2.make_attack()
            victim1.get_hit(damage)
            if victim1.is_dead:
                team1.remove(victim1)
                print()
            else:
                print(victim1, '\n')

    if len(team1) > 0 and len(team2) == 0:
        print(f'End of the fight!\n'
              f'{team1} rozjebal wszystkich!\n'
              f'Fight took {fight_round} rounds.')
        break

    if len(team2) > 0 and len(team1) == 0:
        print(f'End of the fight!\n'
              f'{team2} rozjebal wszystkich!\n'
              f'Fight took {fight_round} rounds.')
        break
