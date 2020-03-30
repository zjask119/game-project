
class Attack:

    def __init__(self, name, power, speed, cost, sacrifice, reduce, _range='target'):
        self.name = name
        self.power = power
        self.speed = speed
        self.initial_power = power
        self.initial_speed = speed
        self.cost = cost
        self.reduce = reduce
        self.range = _range
        self.sacrifice = sacrifice

    def __repr__(self):
        return f'{self.name}, power: {self.power}, cost: {self.cost}'
