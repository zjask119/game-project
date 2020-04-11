
class Attack:

    def __init__(self, name, power, speed, cost, sacrifice, type_, range_):
        self.name = name
        self.power = power
        self.speed = speed
        self.initial_power = power
        self.initial_speed = speed
        self.cost = cost
        self.type = type_
        self.range = range_
        self.sacrifice = sacrifice

        # GUI
        self.id = None

    def __repr__(self):
        return f'{self.name}, power: {self.power}, cost: {self.cost}'
