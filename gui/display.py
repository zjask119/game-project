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

    areas_number = 4
    colors = [GREEN, GREEN_LIGHT, BLUE_LIGHT, BLUE]

    def __init__(self, width, height):
        image_path = IMAGES_DIR.joinpath('background-moon.jpg')
        self.surface = get_image(image_path, (width, height))
        self.areas = []

    def add_area(self, area):
        self.areas.append(area)

    def get_size(self):
        return self.surface.get_size()

    def get_area_size(self):
        """
        @return: tuple (width, height)
        """
        board_w, board_h = self.get_size()
        area_w = int(board_w / self.areas_number)
        return area_w, board_h

    def get_areas(self):
        result = []
        area_w, _ = self.get_area_size()
        for index, area in enumerate(self.areas):
            pos = (index * area_w, 0)
            result.append((pos, area))
        return result


class Area:

    def __init__(self, heroes, area_size):
        self.surface = pygame.Surface(area_size)
        self.heroes = heroes

    def get_size(self):
        return self.surface.get_size()


class HeroZone:

    size = (120, 140)

    def __init__(self, hero):
        self.hero_obj = hero
        self.surface = pygame.Surface(self.size)

        self.hero_image_sprite = HeroImage(hero)
        self.hp_surface = self.create_hp_surface()

        self.draw()

    def create_hp_surface(self):
        width = self.size[0]
        height = 10
        border = 1

        hp_surface = pygame.Surface((width, height))
        hp_surface.set_alpha(200)
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

    def draw(self):
        zone_w, zone_h = self.size
        image_w, image_h = self.hero_image_sprite.surface.get_size()
        hp_bar_w, hp_bar_h = self.hp_surface.get_size()

        self.surface.blit(self.hero_image_sprite.surface, ((zone_w - image_w) / 2,
                                                           (zone_h - image_h + hp_bar_h) / 2))
        self.surface.blit(self.hp_surface, ((zone_w - image_w) / 2,
                                            (zone_h - image_h + hp_bar_h) / 2 - hp_bar_h))


class HeroImage(pygame.sprite.Sprite):
    size = (120, 120)
    border_size = 5

    images_filepath = IMAGES_DIR.joinpath('characters')

    def __init__(self, hero):
        pygame.sprite.Sprite.__init__(self)

        self.hero_obj = hero
        self.surface = self.create_surface(hero)
        self.rect = self.surface.get_rect()

    def create_surface(self, hero):

        filepath = self.images_filepath / hero.img_path

        surface = pygame.Surface(self.size)
        if hero.alive:
            surface.set_alpha(230)
        else:
            surface.set_alpha(120)

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


def prepare_board(board, game):
    area_size = board.get_area_size()
    area_heroes = [
        game.teams[0].get_all_heroes(area=HeroAreaEnum.BACK),
        game.teams[0].get_all_heroes(area=HeroAreaEnum.FRONT),
        game.teams[1].get_all_heroes(area=HeroAreaEnum.FRONT),
        game.teams[1].get_all_heroes(area=HeroAreaEnum.BACK),
    ]
    for heroes in area_heroes:
        area = Area(heroes, area_size)
        board.add_area(area)
        draw_heroes(area)

    for pos, area in board.get_areas():
        board.surface.blit(area.surface, pos)


def draw_heroes(area):

    if not area.heroes:
        return

    area_w, area_h = area.get_size()

    margin_h = 200
    area_h -= margin_h

    distributed_height = area_h / len(area.heroes)

    for num, hero in enumerate(area.heroes):
        hero_sprint = HeroZone(hero)
        point_w, point_h = hero_sprint.size

        x = area_w / 2 - point_w / 2
        y = num * distributed_height + distributed_height / 2 - point_h / 2 + margin_h / 2
        area.surface.blit(hero_sprint.surface, (x, y))


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
            board = Board(SCREEN_WIDTH, SCREEN_HEIGHT)

            prepare_board(board, game)

            screen.blit(board.surface, (0, 0))

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
