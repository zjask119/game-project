import pygame

from config import IMAGES_DIR
from main import run_game
from models.enums import HeroAreaEnum

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (64, 64, 64)

RED = (200, 0, 0)
RED_LIGHT = (255, 0, 0)

GREEN = (0, 128, 0)
GREEN_LIGHT = (51, 204, 51)

BLUE = (0, 51, 153)
BLUE_LIGHT = (0, 77, 230)

GOLD = (230, 184, 0)
ORANGE = (255, 153, 0)
YELLOW = (247, 237, 0)

# screen size
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768


class Board:

    teams_num = 2

    def __init__(self, game, size):
        image_path = IMAGES_DIR.joinpath('background.jpg')
        self.surface = get_image(image_path, size)
        self.game_obj = game
        self.team_zones = []

        self.prepare_team_zones()
        self.draw_team_zones()

    def add_team_zone(self, team_zone):
        self.team_zones.append(team_zone)

    def get_team_zone_size(self):
        """
        @return: tuple (width, height)
        """
        board_w, board_h = self.get_size()
        team_zone_w = int(board_w / self.teams_num)
        return team_zone_w, board_h

    def prepare_team_zones(self):
        team_zones = [
            TeamZone(self.game_obj.teams[0], 'left', self.get_team_zone_size()),
            TeamZone(self.game_obj.teams[1], 'right', self.get_team_zone_size()),
        ]
        for team_zone in team_zones:
            self.add_team_zone(team_zone)

    def draw_team_zones(self):
        team_zone_w, _ = self.get_team_zone_size()
        for index, team_zone in enumerate(self.team_zones):
            pos = (index * team_zone_w, 0)
            self.surface.blit(team_zone.surface, pos)

    def get_size(self):
        return self.surface.get_size()


class TeamZone:

    areas_num = 2

    def __init__(self, team, side, size):
        self.surface = pygame.Surface(size)
        self.team = team
        self.side = side
        self.areas = []

        self.prepare_areas()
        self.draw_areas()
        self.draw_energy()

    def prepare_areas(self):
        zones = [HeroAreaEnum.BACK, HeroAreaEnum.FRONT]
        if self.side == 'right':
            zones = zones[::-1]

        for zone in zones:
            heroes = self.team.get_all_heroes(area=zone, sorted_by=None)
            area = Area(heroes, self.get_area_size())
            self.areas.append(area)

    def get_area_size(self):
        """
        @return: tuple (width, height)
        """
        board_w, board_h = self.get_size()
        area_w = int(board_w / self.areas_num)
        return area_w, board_h

    def draw_areas(self):
        area_w, _ = self.get_area_size()
        for index, area in enumerate(self.areas):
            pos = (index * area_w, 0)
            self.surface.blit(area.surface, pos)

    def draw_energy(self):
        size = 35
        image_path = IMAGES_DIR.joinpath('energy.png')
        energy_surf = get_image(image_path, 2 * (size, ))
        energy = self.team.energy

        for i in range(energy):
            if self.side == 'left':
                w = size / 2
            else:
                team_zone_w, team_zone_h = self.get_size()
                w = team_zone_w - 1.5 * size
            h = size / 2 + 1.5 * size * i
            self.surface.blit(energy_surf, (w, h))

    def get_size(self):
        return self.surface.get_size()


class Area:

    def __init__(self, heroes, area_size):
        self.surface = pygame.Surface(area_size)
        self.heroes = heroes
        self.draw_heroes()

    def draw_heroes(self):
        if not self.heroes:
            return

        area_w, area_h = self.get_size()

        margin_h = 100
        area_h -= margin_h

        distributed_height = area_h / len(self.heroes)

        for num, hero in enumerate(self.heroes):
            hero_sprint = HeroZone(hero)
            point_w, point_h = hero_sprint.size

            x = area_w / 2 - point_w / 2
            y = num * distributed_height + distributed_height / 2 - point_h / 2 + margin_h / 2
            self.surface.blit(hero_sprint.surface, (x, y))

    def get_size(self):
        return self.surface.get_size()


class HeroZone:

    size = (150, 120)

    def __init__(self, hero):
        self.hero_obj = hero
        self.surface = pygame.Surface(self.size)

        self.hero_image_sprite = HeroImage(hero)
        self.hp_surface = self.create_hp_surface()

        self.draw_hero_hp()
        self.draw_icons()

    def create_hp_surface(self):
        width = self.hero_image_sprite.size[0]
        height = 10
        border = 1

        hp_surface = pygame.Surface((width, height))
        hp_surface.set_alpha(220)
        hp_surface.fill(BLACK)

        colors = [RED, ORANGE, YELLOW, GREEN_LIGHT]
        ratio = self.hero_obj.hp / self.hero_obj.initial_hp
        if ratio == 1:
            color_idx = len(colors) - 1
        else:
            color_idx = int(ratio * len(colors))
        color = colors[color_idx]

        bar_h = height - 2 * border

        left_w = int(width * ratio) - 2 * border
        if left_w > 0:
            left_bar = pygame.Surface((left_w, bar_h))
            left_bar.fill(color)
            hp_surface.blit(left_bar, (border, border))

        return hp_surface

    def draw_icons(self):
        max_num_of_icons = 2
        icon_h = 30
        inactive_icon_alpha = 150

        zone_w, zone_h = self.size
        img_w, _ = self.hero_image_sprite.size

        icon_w = int(0.75 * icon_h)
        stun = get_image(IMAGES_DIR.joinpath('stun.png'), (icon_w, icon_h)).convert_alpha()
        shield = get_image(IMAGES_DIR.joinpath('shield.png'), (icon_w, icon_h)).convert_alpha()

        distributed_height = zone_h / max_num_of_icons

        w = img_w + (zone_w - img_w - icon_w) / 2

        h = 0 * distributed_height + distributed_height / 2 - icon_h / 2
        if not self.hero_obj.stunned:
            stun.set_alpha(inactive_icon_alpha)
        self.surface.blit(stun, (w, h))

        h = 1 * distributed_height + distributed_height / 2 - icon_h / 2
        if self.hero_obj.shield == 0:
            shield.set_alpha(inactive_icon_alpha)
        self.surface.blit(shield, (w, h))

    def draw_hero_hp(self):
        zone_w, zone_h = self.size
        image_w, image_h = self.hero_image_sprite.surface.get_size()
        hp_bar_w, hp_bar_h = self.hp_surface.get_size()

        self.surface.blit(self.hero_image_sprite.surface, (0, (zone_h - image_h + hp_bar_h) / 2))
        self.surface.blit(self.hp_surface, (0, (zone_h - image_h + hp_bar_h) / 2 - hp_bar_h))


class HeroImage(pygame.sprite.Sprite):
    size = 2 * (100, )
    border_size = 3

    images_filepath = IMAGES_DIR.joinpath('characters')

    def __init__(self, hero):
        pygame.sprite.Sprite.__init__(self)

        self.hero_obj = hero
        self.surface = self.create_surface(hero)
        self.rect = self.surface.get_rect()

    def create_surface(self, hero):

        filepath = self.images_filepath / hero.img_path

        surface = pygame.Surface(self.size)
        if not hero.alive:
            surface.set_alpha(150)

        if self.hero_obj.active:
            surface.fill(GOLD)
        elif self.hero_obj.victim:
            surface.fill(RED)
        else:
            surface.fill(GREY)

        img_size = tuple(x - y for x, y in zip(self.size, 2 * (2 * self.border_size, )))
        image = get_image(filepath, img_size).convert_alpha()

        surface.blit(image, 2 * (self.border_size, ))

        return surface


def get_image(filepath, img_size=None):
    from pathlib import Path

    if isinstance(filepath, Path):
        filepath = str(filepath)

    img = pygame.image.load(filepath)
    if img_size:
        img = pygame.transform.scale(img, img_size)

    return img


def main():
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Amazing Game')

    clock = pygame.time.Clock()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for game in run_game():
            board = Board(game, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(board.surface, (0, 0))

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
