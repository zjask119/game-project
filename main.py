import displayer
from models.game import Game
from utils import assign_heroes_to_team, get_heroes_from_db, prepare_teams


def run_game():

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

        yield game

        def get_characters(char, num): return ''.join(num * [char])
        displayer.print_error(
            f'{get_characters(">", 30)} Round {game_round} {get_characters("<", 30)}\n'.center(152))

        for active_hero in game.get_alive_heroes():
            if not active_hero.alive:
                continue

            active_hero.active = True

            displayer.print_teams(game)
            print(
                f'{active_hero.team.name} move [ENERGY: {active_hero.team.energy}] '
                f'- {active_hero.name} is taking action.'
            )
            active_team = active_hero.team
            target_team = team2 if active_team == team1 else team1

            yield game

            active_hero.take_action(target_team)

            yield game

            game.reset_attributes()

            # if active_hero.team.npc:
            input('Press any button to continue...')

            if not team1.is_anybody_alive():
                print(f'{team2.name} won!')
                break

            if not team2.is_anybody_alive():
                print(f'{team1.name} won!')
                break


if __name__ == "__main__":
    for _ in run_game():
        pass
