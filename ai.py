from board import *
import random

# randomly find a shot
def shot_random(board):
    size = board.get_size()
    x = random.randint(0, size-1)
    y = random.randint(0, size-1)
    while board.get_box_status([x,y]) == Status.hit or board.get_box_status([x,y]) == Status.miss:
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
    if board.get_box_status([x,y]) == Status.ship:
        board.set_box_status([x,y], Status.hit)
    else:
        board.set_box_status([x,y], Status.miss)

def get_prob_board(board, ships):
    boardCopy = board.get_board_copy()
    probBoard = Board(startStatus=0)
    size = boardCopy.get_size()
    for ship in ships:
        for row in range(size):
            for col in range(size):
                location = [col, row]
                if boardCopy.set_ship_at(location, ship, ShipAlignment.leftToRight) == 0:
                    boardCopy = board.get_board_copy()
                    for x in range(ship):
                        probBoard.set_box_status([col + x, row], probBoard.get_box_status([col + x, row]) + 1)
                if boardCopy.set_ship_at(location, ship, ShipAlignment.upToDown) == 0:
                    boardCopy = board.get_board_copy()
                    for x in range(ship):
                        probBoard.set_box_status([col, row + x], probBoard.get_box_status([col, row + x]) + 1)
                if boardCopy.set_ship_at(location, ship, ShipAlignment.downToUp) == 0:
                    boardCopy = board.get_board_copy()
                    for x in range(ship):
                        probBoard.set_box_status([col, row - x], probBoard.get_box_status([col, row - x]) + 1)
                if boardCopy.set_ship_at(location, ship, ShipAlignment.rightToLeft) == 0:
                    boardCopy = board.get_board_copy()
                    for x in range(ship):
                        probBoard.set_box_status([col - x, row], probBoard.get_box_status([col - x, row]) + 1)
    return probBoard

def pick_next_prob_hit(board, ships):
    hits = board.get_board_ships(status=Status.hit)
    probBoard = get_prob_board(board, ships)
    best = 0
    bestLoc = []
    for row in range(probBoard.get_size()):
        for col in range(probBoard.get_size()):
            if best < probBoard.get_box_status([col, row]):
                best = probBoard.get_box_status([col, row])
                if [col, row] not in hits:
                    bestLoc = [col, row]
    return bestLoc

def pick_next_hit(board, ships):
    hits = board.get_board_ships(status=Status.hit)
    if len(hits) == 0:
        return pick_next_prob_hit(board, ships)
    misses = board.get_board_ships(status=Status.miss)
    next = []

    for hit in hits:
        if hit[0] - 1 >= 0:
            loc = [hit[0] -1, hit[1]]
            if loc not in misses and loc not in hits:
                next.append(loc)
        if hit[0] + 1 < board.get_size():
            loc = [hit[0] + 1, hit[1]]
            if loc not in misses and loc not in hits:
                next.append(loc)
        if hit[1] - 1 >= 0:
            loc = [hit[0], hit[1] - 1]
            if loc not in misses and loc not in hits:
                next.append(loc)
        if hit[1] + 1 < board.get_size():
            loc = [hit[0], hit[1] + 1]
            if loc not in misses and loc not in hits:
                next.append(loc)
    probBoard = get_prob_board(board, ships)
    best = 0
    bestLoc = []
    for spot in next:
        if probBoard.get_box_status(spot) > best:
            best = probBoard.get_box_status(spot)
            bestLoc = spot
    if bestLoc == []:
        return pick_next_prob_hit(board, ships)
    return bestLoc
