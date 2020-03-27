from termcolor import cprint


def print_teams(game):
    def _get_line_separator(n=150):
        return '+'.ljust(n, '-') + '+\n'

    def _wrap_content(data, n=150, new_line=True, line_separator=True):
        if isinstance(data, str):
            to_add = n - divmod(n, 2)[1] - 1
            msg = '|' + str(data).center(to_add) + '|'
        elif isinstance(data, list):
            to_add = int(n / len(data)) - 1
            msg = '|' + '|'.join(str(content).center(to_add)
                                 for content in data) + '|'
        else:
            raise NotImplementedError

        if new_line:
            msg += '\n'
        if line_separator:
            msg += _get_line_separator()
        return msg

    msg = ''
    msg += _get_line_separator()
    msg += _wrap_content('TEAMS', )
    msg += _wrap_content([team.name for team in game.teams], )
    msg += _wrap_content(2 * ['name', 'HP', 'defence', 'speed', 'area'])

    max_heroes_len = max([len(team.heroes) for team in game.teams])
    for i in range(max_heroes_len):
        heroes = [team.get_all_heroes()[i] for team in game.teams]
        heroes_info = []
        for hero in heroes:
            heroes_info.extend([hero.name, hero.hp,
                                hero.defence, hero.speed, hero.area])
        msg += _wrap_content(heroes_info, line_separator=False)
    msg += _get_line_separator()
    print(msg)


def custom_print_bold(text, colour):
    return cprint(text, colour, attrs=['bold'])
