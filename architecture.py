from typing import List

class Player:


    class Team:

        def __init__(self, energy: int, front_line: List, support_line: List):
            self.energy  = energy
            self.front_line = front_line
            self.support_line = support_line


        class Hero:

            def __init__(self, name: str, hp: float, defen: float, speed: float, mind: int):
                self.name = name
                self.hp = hp
                self.defen = defen
                self.speed = speed
                self.mind = mind
                self.is_alive = True

            def __str__(self):
                return f'Hero: {self.name} with Hp: {self.hp}'


            class Move:

                def __init__(self, name: str, value: float, cost: int):
                    self.name = name
                    self.value = value
                    self.cost = cost

                def attack(self):  # wojownik atakuje pojedynczego przeciwnika
                    pass # return damage

                def area_attack(self):  # wojownik atakuje wszystkich przeciwników w jednej strefie
                    pass # return damage

                def heal(self):  # wojownik ulecza sam siebie
                    pass

                def party_heal(self):  # wojownik ulecza całą swoją druzynę
                    pass

                def barrier(self):  # wojownik rozposciera barierę przed sobą do konca trwania obecnej tury
                    pass # defen x4

                def party_barrier(self):  # wojownik rozposciera barierę przed wszystkimi w swojej strefie - obecna tura
                    pass # defen całej druzyny x4

                def teleport(self):  # do konca obecnej tury wojownik unika wszystkich ataków wymierzonych w niego
                    pass

                def boost(self):  # wojownik zwiększa limit energii do wykorzystania dla swojej druzyny w obecnej turze o 1
                    pass


            def reduce_stats(self):
                pass

            def reduce_hp(self):
                pass

            def get_hit(self):
                pass

            def critical(self):
                # critical_value = attack.value x 1.5
                # chance = 0
                # mind to wartość z przedziału 1 - 100
                # if player1.mind > player2.mind:
                #   chance = player1.mind - player2.mind
                #   chance = chance * 0.01
                #   return chance

            def dodge(self):
                # chance = 0
                # if player1.speed > player2.speed:
                #   chance = player2.speed / player1.speed
                #   return chance

            @property
            def is_dead(self):
                return not self.is_alive
