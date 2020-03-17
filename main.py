import displayer
from models.enums import HeroAreaEnum
from models.game import Game
from utils import prepare_teams


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
                area_num = int(
                    input(f'Choose area (number) for hero {hero.name}: '))
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

        comp_team.energy = 0
        game_round += 1

        energy = 2 * game_round
        human_team.set_energy(energy)
        comp_team.set_energy(energy)

        get_characters = lambda char, num: ''.join(num * [char])
        displayer.custom_print_bold(
            f'{get_characters(">", 30)} Round {game_round} {get_characters("<", 30)}\n'.center(152), 'red')

        for striker_hero in game.get_alive_heroes():
            if not striker_hero.alive:
                continue

            displayer.print_teams(game)
            print(
                f'{striker_hero.name} is attacking. Energy status: {striker_hero.team.energy}')

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

        human_team.reduce_heroes_attributes()
        comp_team.reduce_heroes_attributes()


if __name__ == "__main__":
    main()
