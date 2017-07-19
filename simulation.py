from board import *
from ai import *

# Length of all ships
ships = [4,3,3,2]

# creates ships in random locations
def create_enemy_board():
    board = Board(owner='enemy')
    size = board.get_size()
    x = random.randint(0, size)
    y = random.randint(0, size)
    for ship in ships:
        align = random.choice(list(ShipAlignment))
        while (board.set_ship_at([x,y], ship, align)):
            x = random.randint(0, size)
            y = random.randint(0, size)
            align = random.choice(list(ShipAlignment))
    return board

shotB = Board()

shotLog = []

locs = Location("a1")
while len(ships) > 0:
    nextShot = pick_next_hit(shotB, ships)
    print(locs.get_letter(nextShot))
    response = input("hit(y/Y) ")
    if response.upper() == "Y":
        shotB.set_box_status(nextShot, Status.hit)
    else:
        shotB.set_box_status(nextShot, Status.miss)
    print(shotB)
    response = input("ship to remove: ")
    try:
        ships.remove(int(response))
    except:
        continue