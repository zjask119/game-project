# statystyki walczących wojowników,
# muszą być stałe, aby zmienne generowane w czasie walki mogłby się do nich odnosić

# PLAYER 1          100
h = 258.0
a = 75.0
v = 52.0

# PLAYER 2          90

hp = 252.0
at = 79.0
vi = 48.0

# zmienne generowane w trakcie walki, przed walką mają takie same wartości jak statystyki stałe

h2 = h
hp2 = hp
a2 = a
v2 = v
at2 = at
vi2 = vi
count = 0

# x oznacza damage który zadaje player 1, y to damage który zadaje player 2, przed walką wynoszą 0

x = 0
y = 0

print(f'{count}. player 1: \t {h2},\t{a2},\t{v2} \t player 2: \t{hp2},\t{at2},\t{vi2}') # statystyki obu przed walką

while h2 > h * 0.01 or hp2 > hp * 0.01:
    count += 1
    if a2 - vi2 > 0:
        x = x + a2 - vi2
    else:
        x = x
    x = max(x, 0)
    d = 1 - x / hp
    d = max(d, 0)
    d = d**0.5
    if at2 - v2 > 0:
        y = y + at2 - v2
    else:
        y = y
    y = max(y, 0)
    dm = 1 - y / h
    dm = max(dm, 0)
    dm = dm**0.5
    at2 = at * d
    at2 = round(at2, 2)
    vi2 = vi * d
    vi2 = round(vi2, 2)
    a2 = a * dm
    a2 = round(a2, 2)
    v2 = v * dm
    v2 = round(v2, 2)
    hp2 = hp - x
    hp2 = round(hp2, 2)
    if hp2 < 0:
        hp2 = 0
        print(f'{count}. player 1: \t {h2},\t{a2},\t{v2} \t player 2: \t{hp2},\t{at2},\t{vi2}')
        print('Player 1 won.')
        break
    h2 = h - y
    h2 = round(h2, 2)
    if h2 < 0:
        h2 = 0
        print(f'{count}. player 1: \t {h2},\t{a2},\t{v2} \t player 2: \t{hp2},\t{at2},\t{vi2}')
        print('Player 2 won.')
        break
    print(f'{count}. player 1: \t {h2},\t{a2},\t{v2} \t player 2: \t{hp2},\t{at2},\t{vi2}')
