from functools import partial

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
    msg += _wrap_content(2 * ['name', 'HP', 'defence', 'shield', 'speed', 'area'])

    max_heroes_len = max([len(team.heroes) for team in game.teams])
    for i in range(max_heroes_len):
        heroes = [team.get_all_heroes()[i] for team in game.teams]
        heroes_info = []
        for hero in heroes:
            heroes_info.extend([hero.name, hero.hp, hero.defence,
                               hero.shield, hero.speed, hero.area])
        msg += _wrap_content(heroes_info, line_separator=False)
    msg += _get_line_separator()
    print(msg)


print_error = partial(cprint, color='red', attrs=['bold'])


def get_row_str(proportions, data):
    data = list(zip(proportions, data))
    content = [''.join(str(x[1]).center(x[0])) for x in data]
    return "|" + "|".join(content) + "|"


def get_line_str(proportions):
    chars = [''.join(p * ['-']) for p in proportions]
    line = '+' + '+'.join(chars) + '+'
    return line


def print_table(data, fields, proportions, with_indices=True):
    if data:
        for attr in fields:
            assert hasattr(data[0], attr)

    new_data = []
    for idx, obj in enumerate(data, 1):
        row = [getattr(obj, field) for field in fields]
        if with_indices:
            row.insert(0, idx)
        new_data.append(row)

    if with_indices:
        fields.insert(0, 'No')

    assert len(fields) == len(proportions)

    msg = get_line_str(proportions) + '\n'
    msg += get_row_str(proportions, fields) + '\n'
    msg += get_line_str(proportions) + '\n'
    for row in new_data:
        msg += get_row_str(proportions, row) + '\n'
    msg += get_line_str(proportions) + '\n'
    print(msg)


def print_moves(moves, with_indices=True):
    proportions = [4, 30, 11, 11, 11, 11, 11, 6]
    fields = ['name', 'power', 'speed', 'sacrifice', 'type', 'range', 'cost']
    print_table(moves, fields, proportions, with_indices)


def print_heroes(heroes, with_indices=True):
    proportions = [4, 30, 11, 11, 11, 11]
    fields = ['name', 'hp', 'defence', 'speed', 'area']
    print_table(heroes, fields, proportions, with_indices)


def print_hero_areas(areas):
    proportions = [7, 10]
    fields = ['value', 'name']
    print_table(areas, fields, proportions, with_indices=False)
