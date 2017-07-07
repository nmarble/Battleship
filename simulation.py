from Board import *
from AI import *

# Length of all ships
ships = [5,4,3,2]

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

# create both board with random ships
enemyB = create_enemy_board()
playerB = create_enemy_board()

# determine how many hits are needed to win
maxhit = 0
for ship in ships:
    maxhit = maxhit + ship

# shoot randomly until at least one is finished
while enemyB.get_total_status(Status.hit) < maxhit and playerB.get_total_status(Status.hit) < maxhit:
    shot_random(enemyB)
    shot_random(playerB)

# Display results
enemyHits = enemyB.get_total_status(Status.hit)
enemyMiss = enemyB.get_total_status(Status.miss)
print(enemyB)
print("enemy hits = " + str(enemyHits))
print("enemy misses = " + str(enemyMiss))
print("accuracy = " + str(float(enemyHits) / float(enemyHits+enemyMiss)))

playerHits = playerB.get_total_status(Status.hit)
playerMiss = playerB.get_total_status(Status.miss)
print(playerB)
print("player hits = " + str(playerHits))
print("player misses = " + str(playerMiss))
print("accuracy = " + str(float(playerHits) / float(playerHits+playerMiss)))
