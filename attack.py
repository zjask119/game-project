
class Attack:

    def __init__(self, name, power, speed, cost=0, victim='target', sacrifice=0):
        self.name = name
        self.power = power
        self.speed = speed
        self.cost = cost
        self.victim = victim
        self.sacrifice = sacrifice

    def __repr__(self):
        return f'{self.name}, power: {self.power}, cost: {self.cost}'

