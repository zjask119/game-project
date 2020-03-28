
class Attack:

    def __init__(self, name, power, speed, cost=0, reduce=True, _range='target', sacrifice=0):
        self.name = name
        self.power = power
        self.speed = speed
        self.cost = cost
        self.reduce = reduce
        self.range = _range
        self.sacrifice = sacrifice

    def __repr__(self):
        return f'{self.name}, power: {self.power}, cost: {self.cost}'
