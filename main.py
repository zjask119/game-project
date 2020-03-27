import displayer
from models.game import Game
from utils import assign_heroes_to_team, get_heroes_from_db, prepare_teams


def main():

    heroes = get_heroes_from_db()
    team1, team2 = prepare_teams()
    assign_heroes_to_team(heroes, team1)
    assign_heroes_to_team(heroes, team2)

    game = Game(teams=[team1, team2])

    print(f'\nThe fight between:\n'
          f'{team1}\n'
          f'and\n'
          f'{team2}\n'
          f'has begun...')

    game_round = 0

    while team1.is_anybody_alive() and team2.is_anybody_alive():

        team2.energy = 0
        game_round += 1

        energy = 2 * game_round
        team1.set_energy(energy)

        team2.set_energy(energy)

        def get_characters(char, num): return ''.join(num * [char])
        displayer.custom_print_bold(
            f'{get_characters(">", 30)} Round {game_round} {get_characters("<", 30)}\n'.center(152), 'red')

        for striker_hero in game.get_alive_heroes():
            if not striker_hero.alive:
                continue

            displayer.print_teams(game)
            print(
                f'{striker_hero.team.name} - {striker_hero.name} is attacking. Energy status: {striker_hero.team.energy}')

            if striker_hero.team == team1:
                enemy_team = team2
            else:
                enemy_team = team1

            victim_hero = game.choose_victim(enemy_team)
            striker_hero.attack_hero(victim_hero)

            if not team1.is_anybody_alive():
                print(f'{team2.name} won!')
                break

            if not team2.is_anybody_alive():
                print(f'{team1.name} won!')
                break

        team1.reduce_heroes_attributes()
        team2.reduce_heroes_attributes()


if __name__ == "__main__":
    main()
