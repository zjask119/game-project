import pygame

from config import IMAGES_DIR
from main import run_game
from models.enums import HeroAreaEnum

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (200, 0, 0)
RED_LIGHT = (255, 0, 0)

GREEN = (0, 128, 0)
GREEN_LIGHT = (51, 204, 51)

BLUE = (0, 51, 153)
BLUE_LIGHT = (0, 77, 230)

# screen size
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768


class Board:

    areas_number = 4
    colors = [GREEN, GREEN_LIGHT, BLUE_LIGHT, BLUE]

    def __init__(self, width, height):
        image_path = IMAGES_DIR.joinpath('background.png')
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


class Hero(pygame.sprite.Sprite):
    size = (80, 80)
    images_filepath = IMAGES_DIR.joinpath('characters')

    def __init__(self, image_filename):
        pygame.sprite.Sprite.__init__(self)

        filepath = self.images_filepath / image_filename

        self.surface = get_image(filepath, self.size)
        self.rect = self.surface.get_rect()

    def get_size(self):
        return self.surface.get_size()


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
        draw_points(area)

    for pos, area in board.get_areas():
        board.surface.blit(area.surface, pos)


def draw_points(area):
    margin_h = 200

    area_w, area_h = area.get_size()
    area_h -= margin_h

    distributed_height = area_h / len(area.heroes)
    for num, hero in enumerate(area.heroes):
        point = Hero(hero.img_path)
        point_w, point_h = point.get_size()
        pos = (area_w / 2 - point_w / 2,
               num * distributed_height + distributed_height / 2 - point_h / 2 + margin_h / 2)
        area.surface.blit(point.surface, pos)


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
            clock.tick(0.5)

    pygame.quit()


if __name__ == "__main__":
    main()
