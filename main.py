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

    while team1.is_anybody_alive() and team2.is_anybody_alive():

        game.round += 1

        energy = min(2 * game.round, 8)
        game.prepare_round(energy)

        yield game

        displayer.print_yellow(f'>>> Round {game.round} <<<'.center(190))

        for active_hero in game.get_alive_heroes():
            if not active_hero.alive:
                continue

            displayer.print_teams(game)

            active_hero.active = True
            active_team = active_hero.team
            target_team = team2 if active_team == team1 else team1

            target_team.assign_ids()

            yield game

            active_hero.take_action(target_team)
            target_team.reset_ids()

            yield game

            game.reset_attributes()

            if not team1.is_anybody_alive():
                print(f'{team2.name} won!')
                break

            if not team2.is_anybody_alive():
                print(f'{team1.name} won!')
                break

            input('Press any button to continue...')


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        for _ in run_game():
            pass
    elif len(sys.argv) == 2 and sys.argv[1] == 'gui':
        from gui.display import run_gui

        run_gui()
