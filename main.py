import displayer
from models.game import Game
from utils import assign_heroes_to_team, get_heroes_from_db, prepare_teams


def main():

    heroes = get_heroes_from_db()
    team1, team2 = prepare_teams()
    assign_heroes_to_team(heroes, team1)
    assign_heroes_to_team(heroes, team2)

    game = Game(team1, team2)

    print(f'\nThe fight between:\n'
          f'{team1}\n'
          f'and\n'
          f'{team2}\n'
          f'has begun...')

    game_round = 0

    while team1.is_anybody_alive() and team2.is_anybody_alive():
        game_round += 1

        energy = 2 * game_round
        game.prepare_round(energy)

        def get_characters(char, num): return ''.join(num * [char])
        displayer.print_error(
            f'{get_characters(">", 30)} Round {game_round} {get_characters("<", 30)}\n'.center(152))

        for attacking_hero in game.get_alive_heroes():
            if not attacking_hero.alive:
                continue

            displayer.print_teams(game)
            print(
                f'{attacking_hero.team.name} - {attacking_hero.name} is attacking. '
                f'Energy status: {attacking_hero.team.energy}')

            attacking_team = attacking_hero.team
            enemy_team = team2 if attacking_team == team1 else team1

            if attacking_hero.stunned:
                print(f'{attacking_hero.name} is stunned and cannot move!')
                attacking_hero.stunned = False
                continue

            victim_hero = game.choose_victim(attacking_team, enemy_team)
            attacking_hero.take_action(victim_hero)

            if not team1.is_anybody_alive():
                print(f'{team2.name} won!')
                break

            if not team2.is_anybody_alive():
                print(f'{team1.name} won!')
                break


if __name__ == "__main__":
    main()
