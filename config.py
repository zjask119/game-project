from pathlib import Path

ROOT_DIR = Path(__file__).parent

DB_DIR = ROOT_DIR.joinpath('dragonball.db')
STATIC_DIR = ROOT_DIR.joinpath('static')
IMAGES_DIR = STATIC_DIR.joinpath('images')
ICONS_DIR = IMAGES_DIR.joinpath('icons')
