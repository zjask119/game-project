def damage_calc(damage, attack, toughness):
    if attack - toughness > 0:
        damage += attack - toughness
    damage = max(damage, 0)
    return damage


def reduction_calc(damage, hp):
    reduction = 1 - damage / hp
    reduction = max(reduction, 0)
    reduction = reduction**0.5
    return reduction


def stats_calc(value, reduction):
    stat = value * reduction
    stat = round(stat, 2)
    return stat


def hp_calc(hp, damage):
    hitpoints = hp - damage
    hitpoints = round(hitpoints, 2)
    hitpoints = max(hitpoints, 0)
    return hitpoints
