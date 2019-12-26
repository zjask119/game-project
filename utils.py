from models import Hero, Attack, HeroAreaEnum, Team


def prepare_teams():

    heroes_list_team_1 = [
        Hero('Batman', 200, 40, 76,
             [
                Attack('punch', 51, 76),
                Attack('kick', 57, 72, 1),
                Attack('combo', 62, 75, 2),
             ],
        ),
        Hero('Superman', 210, 40, 85,
             [
                Attack('punch', 78, 80),
                Attack('kick', 82, 82, 1),
                Attack('combo', 99, 85, 2),
             ],
        ),
        Hero('Green Lantern', 180, 30, 78,
             [
                Attack('punch', 80, 73),
                Attack('kick', 84, 79, 1),
                Attack('combo', 300, 85, 2),
             ],
        ),
        Hero('Wonder Woman', 180, 30, 72,
             [
                Attack('punch', 71, 76),
                Attack('kick', 74, 77, 1),
                Attack('combo', 78, 79, 2),
             ],
        ),
    ]

    heroes_list_team_2 = [
        Hero('Spider-Man', 190, 40, 82,
             [
                Attack('punch', 59, 80),
                Attack('kick', 65, 82, 1),
                Attack('combo', 69, 85, 2),
             ],
             HeroAreaEnum.BACK
        ),
        Hero('Thor', 180, 30, 83,
             [
                Attack('punch', 53, 80),
                Attack('kick', 57, 83, 1),
                Attack('combo', 60, 84, 2),
             ],
             HeroAreaEnum.BACK
        ),
        Hero('Iron Man', 190, 40, 71,
             [
                Attack('punch', 51, 70),
                Attack('kick', 57, 72, 1),
                Attack('combo', 63, 77, 2),
             ],
             HeroAreaEnum.FRONT
        ),
        Hero('Hulk', 190, 40, 69,
             [
                Attack('punch', 65, 77),
                Attack('kick', 70, 83, 1),
                Attack('combo', 74, 90, 2),
             ],
             HeroAreaEnum.BACK
        ),
    ]

    return (Team(name='Best team ever', npc=False, heroes=heroes_list_team_1),
            Team(name='Bad guys', npc=True,  heroes=heroes_list_team_2))


def print_teams(game):

    def _get_line_separators(n=150):
        return '+'.ljust(n, '-') + '+\n'

    def _wrap_content(data, n=150, new_line=True):
        if isinstance(data, str):
            to_add = n - divmod(n, 2)[1] - 1
            msg = '|' + str(data).center(to_add) + '|'
        elif isinstance(data, list):
            to_add = int(n / len(data)) - 1
            msg = '|' + '|'.join(str(content).center(to_add) for content in data) + '|'
        else:
            raise NotImplementedError

        if new_line:
            msg += '\n'
        return msg

    msg = ''
    msg += _get_line_separators()
    msg += _wrap_content('TEAMS', )
    msg += _get_line_separators()
    msg += _wrap_content([team.name for team in game.teams], )
    msg += _get_line_separators()
    msg += _wrap_content(2 * ['name', 'HP', 'defence', 'speed', 'area'])
    msg += _get_line_separators()

    max_heroes_len = max([len(team.heroes) for team in game.teams])
    for i in range(max_heroes_len):
        heroes = [team.get_all_heroes()[i] for team in game.teams]
        heroes_info = []
        for hero in heroes:
            heroes_info.extend([hero.name, hero.current_hp, hero.defence, hero.speed, hero.area])
        msg += _wrap_content(heroes_info)
    msg += _get_line_separators()
    print(msg)
