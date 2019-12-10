from models import Hero, Attack, HeroAreaEnum, Team


def prepare_teams():

    heroes_list_team_1 = [
        Hero('Batman', 200, 40, 70,
             [
                Attack('punch', 51, 70),
                Attack('kick', 57, 72, 1),
                Attack('combo', 62, 75, 2),
             ],
        ),
        Hero('Superman', 210, 40, 80,
             [
                Attack('punch', 78, 80),
                Attack('kick', 82, 82, 1),
                Attack('combo', 99, 85, 2),
             ],
        ),
        Hero('Green Lantern', 180, 30, 90,
             [
                Attack('punch', 80, 70),
                Attack('kick', 84, 70, 1),
                Attack('combo', 300, 70, 2),
             ],
        ),
        Hero('Wonder Woman', 180, 30, 70,
             [
                Attack('punch', 71, 76),
                Attack('kick', 74, 77, 1),
                Attack('combo', 78, 79, 2),
             ],
        ),
    ]

    heroes_list_team_2 = [
        Hero('Spider-Man', 190, 40, 80,
             [
                Attack('punch', 59, 80),
                Attack('kick', 65, 82, 1),
                Attack('combo', 69, 85, 2),
             ],
             HeroAreaEnum.BACK
        ),
        Hero('Thor', 180, 30, 80,
             [
                Attack('punch', 53, 80),
                Attack('kick', 57, 83, 1),
                Attack('combo', 60, 84, 2),
             ],
             HeroAreaEnum.BACK
        ),
        Hero('Iron Man', 190, 40, 80,
             [
                Attack('punch', 51, 70),
                Attack('kick', 57, 72, 1),
                Attack('combo', 63, 77, 2),
             ],
             HeroAreaEnum.FRONT
        ),
        Hero('Hulk', 190, 40, 80,
             [
                Attack('punch', 65, 77),
                Attack('kick', 70, 83, 1),
                Attack('combo', 74, 90, 2),
             ],
             HeroAreaEnum.BACK
        ),
    ]

    teams = [
        Team(name='Best team ever!', heroes=heroes_list_team_1),
        Team(name='Bad guys!', heroes=heroes_list_team_2),
    ]

    return teams
