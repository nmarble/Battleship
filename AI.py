from Board import *
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