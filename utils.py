import sqlite3

from models.attack import Attack
from models.hero import Hero


def get_heroes_from_db():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    query = 'select id, name, hp, defence, speed from hero;'
    cursor.execute(query)
    db_heroes = cursor.fetchall()

    query = 'select name, power, speed, cost, constant, user from move;'
    cursor.execute(query)
    db_moves = cursor.fetchall()

    heroes = {}
    moves = []

    for db_hero in db_heroes:
        hero_id, name, hp, defence, speed = db_hero
        hero = Hero(name, hp, defence, speed)
        heroes[hero_id] = hero

    for db_move in db_moves:
        name, power, speed, cost, constant, user = db_move
        cost = cost if cost else 0
        move = Attack(name, power, speed, cost)
        moves.append((user, move))

    for hero_id, move in moves:
        hero = heroes[hero_id]
        if move.speed is None:
            move.speed = hero.speed
        hero.add_move(move)

    return heroes.values()
