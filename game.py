from models import HeroAreaEnum, Game
from utils import prepare_teams, print_teams


def main():
    human_team, comp_team = prepare_teams()
    game = Game(teams=[human_team, comp_team])

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

        human_team.energy = 0
        comp_team.energy = 0
        game_round += 1

        if human_team.energy < 8:
            human_team.energy += 2*game_round

        if comp_team.energy < 8:
            comp_team.energy += 2*game_round

        print(f'-------------------------- Round {game_round} --------------------------\n')

        for striker_hero in game.get_alive_heroes():
            if not striker_hero.alive:
                continue

            print_teams(game)
            print(f'{striker_hero.name} is attacking. Energy status: {striker_hero.team.energy}')

            if striker_hero.team.npc:
                enemy_team = human_team
            else:
                enemy_team = comp_team

            victim_hero = game.choose_victim(enemy_team)
            striker_hero.attack_hero(victim_hero)
            
            if not human_team.is_anybody_alive():
                print('You lost...')
                break

            if not comp_team.is_anybody_alive():
                print('You won!')
                break


if __name__ == "__main__":
    main()
