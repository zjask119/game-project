from collections import defaultdict

import pygame

from config import ICONS_DIR, IMAGES_DIR
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
        self.surface = get_image(image_path, size).convert_alpha()
        self.game_obj = game
        self.team_zones = []

        self.render()

    def add_team_zone(self, team_zone):
        self.team_zones.append(team_zone)

    def get_team_zone_size(self):
        """
        @return: tuple (width, height)
        """
        board_w, board_h = self.get_size()
        team_zone_w = int(board_w / self.teams_num)
        team_zone_h = board_h - MovesZone.height
        return team_zone_w, team_zone_h

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

    def render_round_text(self):
        font_size = 50
        font_alpha = 170

        font = pygame.font.Font(None, font_size)
        text = font.render(f"Round {self.game_obj.round}", True, WHITE)
        text.set_alpha(font_alpha)

        board_w, _ = self.surface.get_size()
        w = (board_w - text.get_width()) / 2
        h = 20
        self.surface.blit(text, (w, h))

    def render_moves_zone(self):
        moves_zone = MovesZone(self.game_obj, self.surface.get_width())
        self.surface.blit(moves_zone.surface, (0, self.surface.get_height() - moves_zone.height))

    def render(self):
        self.prepare_team_zones()
        self.draw_team_zones()
        self.render_round_text()
        self.render_moves_zone()

    def get_size(self):
        return self.surface.get_size()


class MovesZone:

    height = 150

    def __init__(self, game, width):
        self.surface = pygame.Surface((width, self.height))
        # self.surface.set_alpha(230)
        # self.surface.fill(BLACK)
        self.game_obj = game
        self.prepare_moves_surface()

    def prepare_moves_surface(self):
        active_hero = self.game_obj.get_active_hero()
        if not active_hero or active_hero.team.npc:
            return

        num_zones = len(active_hero.moves)
        if not num_zones:
            return

        num_zones = max(num_zones, 4)

        zone_w = int(self.surface.get_width() / num_zones)
        zone_h = self.height
        zone_size = (zone_w, zone_h)

        for i in range(num_zones):
            try:
                move = active_hero.moves[i]
            except IndexError:
                continue
            else:
                move_zone = Move(move, zone_size)
                self.surface.blit(move_zone.surface, (i * zone_w, 0))


class Move:

    def __init__(self, move, size):
        self.surface = pygame.Surface(size)
        self.move_obj = move

        self.render()

    def get_icon_filename(self):

        type_ = self.move_obj.type
        range_ = self.move_obj.range

        icon_map = {
            ('attack', 'area'): 'attack_area.png',
            ('attack', 'target'): 'attack_target.png',
            ('attack const', 'area'): 'attack_const_area.png',
            ('attack const', 'target'): 'attack_const_target.png',
            ('attack stun', 'area'): 'stun_area.png',
            ('drain', 'target'): 'drain_target.png',
            ('heal', 'self'): 'heal_self.png',
            ('heal', 'self area'): 'heal_self_area.png',
            ('heal', 'target'): 'heal_target.png',
            ('shield', 'self'): 'shield_self.png',
            ('shield', 'self area'): 'shield_self_area.png',
            ('stun', 'target'): 'stun_target.png',
        }

        return icon_map[(type_, range_)]

    def get_move_surf(self):
        move_icon_diameter = 80

        filename_abs = ICONS_DIR.joinpath(self.get_icon_filename())
        icon_surf = get_image(filename_abs, 2 * (move_icon_diameter, ))

        return icon_surf

    def get_cost_surf(self):
        icon_size = 25
        icons_interval = 3

        cost = self.move_obj.cost
        cost_surf = get_image(ICONS_DIR.joinpath('energy.png'), 2 * (icon_size, ))  # noqa
        surf = pygame.Surface((cost * (icon_size + icons_interval), icon_size))
        for k in range(cost):
            surf.blit(cost_surf, (k * (icon_size + icons_interval), 0))

        return surf

    def get_move_name_surf(self):
        font_size = 30
        font_alpha = 230
        font = pygame.font.SysFont(None, font_size)
        text = font.render(str(self.move_obj.name), True, WHITE)
        text.set_alpha(font_alpha)

        return text

    def get_move_id_surf(self):
        font_size = 30
        font_alpha = 230
        font = pygame.font.SysFont(None, font_size)
        text = font.render(str(self.move_obj.id), True, WHITE)
        text.set_alpha(font_alpha)

        return text

    def render(self):
        zone_w, zone_h = self.get_size()
        left_margin = 50

        move_surf = self.get_move_surf()
        move_icon_w, move_icon_h = move_surf.get_size()
        pos_x = left_margin
        pos_y = (zone_h - move_icon_h) / 2

        self.surface.blit(move_surf, (pos_x, pos_y))

        cost_surf = self.get_cost_surf()
        cost_surf_w, cost_surf_h = cost_surf.get_size()

        pos_x = left_margin + (move_icon_w - cost_surf_w) / 2
        pos_y = ((zone_h - move_icon_h) / 2 - cost_surf_h - 10)
        self.surface.blit(cost_surf, (pos_x, pos_y))

        move_name_surf = self.get_move_name_surf()
        move_name_surf_w, move_name_surf_h = move_name_surf.get_size()
        pos_x = left_margin + move_icon_w + 10
        pos_y = ((zone_h - move_name_surf_h) / 2)
        self.surface.blit(move_name_surf, (pos_x, pos_y))

        move_id_surf = self.get_move_id_surf()
        move_id_surf_w, move_id_surf_h = move_id_surf.get_size()
        pos_x = left_margin - move_id_surf_w - 10
        pos_y = ((zone_h - move_id_surf_h) / 2)
        self.surface.blit(move_id_surf, (pos_x, pos_y))

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
        image_path = ICONS_DIR.joinpath('energy.png')
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

            w = area_w / 2 - point_w / 2
            h = num * distributed_height + distributed_height / 2 - point_h / 2 + margin_h / 4
            self.surface.blit(hero_sprint.surface, (w, h))

    def get_size(self):
        return self.surface.get_size()


class HeroZone:

    size = (180, 120)

    def __init__(self, hero):
        self.hero_obj = hero
        self.surface = pygame.Surface(self.size)

        self.hero_image_sprite = HeroImage(hero)
        self.hp_surface = self.create_hp_surface()

        self.draw_hero_img_hp()
        self.draw_icons()
        self.draw_hero_id()

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
        icon_size = 35
        inactive_icon_alpha = 150

        zone_w, zone_h = self.size
        img_w, _ = self.hero_image_sprite.size

        stun = get_image(ICONS_DIR.joinpath('stun_target.png'), 2 * (icon_size, )).convert_alpha()
        shield = get_image(ICONS_DIR.joinpath('shield_self.png'), 2 * (icon_size, )).convert_alpha()

        distributed_height = zone_h / max_num_of_icons

        w = img_w + (zone_w - img_w - icon_size) / 2 + 5
        h = distributed_height / 2 - icon_size / 2
        if not self.hero_obj.stunned:
            stun.set_alpha(inactive_icon_alpha)
        self.surface.blit(stun, (w, h))

        h += distributed_height
        if self.hero_obj.shield == 0:
            shield.set_alpha(inactive_icon_alpha)
        self.surface.blit(shield, (w, h))

    def draw_hero_id(self):
        font_size = 53
        font_alpha = 240

        if self.hero_obj.id:
            font = pygame.font.Font(None, font_size)
            text = font.render(str(self.hero_obj.id), True, WHITE)
            text.set_alpha(font_alpha)

            _, hero_zone_h = self.surface.get_size()
            w = 0
            h = (hero_zone_h - text.get_height()) / 2
            self.surface.blit(text, (w, h))

    def draw_hero_img_hp(self):
        zone_w, zone_h = self.size
        image_w, image_h = self.hero_image_sprite.surface.get_size()
        hp_bar_w, hp_bar_h = self.hp_surface.get_size()

        self.surface.blit(self.hero_image_sprite.surface, (20, (zone_h - image_h + hp_bar_h) / 2))
        self.surface.blit(self.hp_surface, (20, (zone_h - image_h + hp_bar_h) / 2 - hp_bar_h))


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


def run_gui():
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
    run_gui()
