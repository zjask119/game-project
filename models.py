class Hero:

    def __init__(self, name: str, hp: float, defence: float, attack: float, speed: float, area: str):
        self.name = name
        self.hp = hp
        self.defence = defence
        self.attack = attack
        self.speed = speed
        self.area = area
        self.is_alive = True

    def __repr__(self):
        return f'{self.name} with Hp: {self.hp}, area: {self.area}'
