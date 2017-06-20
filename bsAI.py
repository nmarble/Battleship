#!/usr/bin/python
import logging
import random

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

valid = [-1,0,1]

def get_best_shot(userBoard, enemyBoard):
    if (check_board(userBoard, "User") or check_board(enemyBoard, "Enemy")) != 0:
        return logging.error('Board check failed')
    
    return 0
        
def check_board(board, name):
    
    if type(board) is not list:
        return logging.error('Incorrect value for %s board: expecting list' % name)
    if len(board) != 10:
        return logging.error('%s board has incorrect amount of rows: expecting 10' % name)
    for row in board:
        if len(row) != 10:
            return logging.error('%s has incorrect amount of columns in row %s: expecting 10' % (name, str(row)))    
        for col in row:
            if col not in valid:
                return logging.error('Invalid value of %s found in %s' % (str(col), name))
    logging.debug('Board check passed')
    return 0

def get_value_at(x,y,board):
    try:
        return board[y][x]
    except:
        return logging.info('Invalid coordinates')
    
def get_random_unshot_loc(board):
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    
    while (get_value_at(x,y, board) != 0):
        x = random.randint(0, 9)
        y = random.randint(0, 9)

    return [x,y] 
