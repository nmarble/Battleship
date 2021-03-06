from enum import Enum
from string import ascii_uppercase
import copy
import itertools

# used to determine the status of the box
class Status(Enum):
    miss = -3
    hit = -2
    empty = 0
    ship = -1

# used in conjunction with setting ship for easy readabilty
class ShipAlignment(Enum):
    leftToRight = 0
    upToDown = 1
    rightToLeft = 2
    downToUp = 3

# Changes word locations into list coords IE: b3 to [1, 2]
class Location(object):

    # Create number associations with each letter
    values = dict()
    for index, letter in enumerate(ascii_uppercase):
        values[letter] = index + 1

    def __init__(self, name):
        self.name = name

    # return list based on values already determined
    def get_coords(self):
        return [int(list(self.name)[1]) - 1, self.values[list(self.name)[0]] - 1, ]

    def get_letter(self, coords):
        for value in self.values:
            if self.values[value] == coords[1] + 1:
                return value + str(coords[0] + 1)
        return "unknown loc"
# main board object
class Board(object):

    # size is used for x by x, owner can be used for determine what to display
    def __init__(self, size=6, owner='user', startStatus=Status.empty):
        self.board = []
        self.owner = owner
        self.size = size
        self.startStatus = startStatus
        self.build_board()


    # set all boxes to empty
    def build_board(self):
        for x in range(0, self.size):
            row = []
            for y in range(0, self.size):
                row.append(self.startStatus)
            self.board.append(row)

    # for easy displaying in text
    def __str__(self):
        board = self.board
        tempBoard = ""
        for row in board:
            tempRow = []
            for col in row:
                if hasattr(col, 'value'):
                    tempRow.append(col.value)
                else:
                    tempRow.append(col)
            tempBoard = tempBoard + str(tempRow) + "\n"

        return str(tempBoard)

    def get_board(self):
        return self.board

    def get_board_single(self):
        return list(itertools.chain.from_iterable(self.board))

    # returns status of box can use list coords or letter("C3")
    def get_box_status(self, loc):
        coords = []
        if type(loc) is str:
            coords = Location(loc).get_coords()
        else:
            coords = loc
        return self.board[coords[1]][coords[0]]

    def get_board_ships(self, status=Status.ship):
        ships = []
        for row in range(0, self.size):
            for col in range(0, self.size):
                if self.get_box_status([row, col]) == status:
                    ships.append([row, col])
        return ships

    def get_board_ships_single(self, status=Status.ship):
        ships = self.get_board_ships(status)
        returnShips = []
        for ship in ships:
            returnShips.append((ship[0] * self.size) + ship[1])
        return returnShips

    # sets status of box can use list coords or letter("C3") for loc
    def set_box_status(self, loc, newStatus):
        if type(loc) is str:
            coords = Location(loc).get_coords()
            self.board[coords[1]][coords[0]] = newStatus
        elif type(loc) is list:
            self.board[loc[1]][loc[0]] = newStatus

    # Determine total number of given status
    def get_total_status(self, status):
        total = 0
        for x in range(0, self.size):
            for y in range(0, self.size):
                if self.get_box_status([x,y]) == status:
                    total = total + 1
        return total

    def get_owner(self):
        return self.owner

    def set_owner(self, newOwner):
        self.owner = newOwner

    def get_size(self):
        return self.size

    # Used to ignore references
    def get_board_copy(self):
        return copy.deepcopy(self)

    # Attempt to set ship at location, with a set size given the alignment
    def set_ship_at(self, loc, size, alignment):
        coords = []
        validStates = [Status.hit, Status.empty]
        # copy board for working with
        tempBoard = self.get_board_copy()
        if type(loc) is str:
            coords = Location(loc).get_coords()
        else:
            coords = loc

        if alignment == ShipAlignment.leftToRight:
            try:
                for col in range(coords[0], coords[0] + size):
                    if col < 0 or col > self.size:
                        return 1
                    if self.get_box_status([col, coords[1]]) in validStates:
                        tempBoard.set_box_status([col, coords[1]], Status.ship)
                    else:
                        return 1
            except:
                return 1
        elif alignment == ShipAlignment.rightToLeft:
            try:
                for col in range(coords[0] - (size - 1), coords[0] + 1):
                    if col < 0 or col > self.size:
                        return 1
                    if self.get_box_status([col, coords[1]]) in validStates:
                        tempBoard.set_box_status([col, coords[1]], Status.ship)
                    else:
                        return 1
            except:
                return 1
        elif alignment == ShipAlignment.upToDown:
            try:
                for row in range(coords[1], coords[1] + size):
                    if row < 0 or row > self.size:
                        return 1
                    if self.get_box_status([coords[0], row]) in validStates:
                        tempBoard.set_box_status([coords[0], row], Status.ship)
                    else:
                        return 1
            except:
                return 1
        elif alignment == ShipAlignment.downToUp:
            try:
                for row in range(coords[1] - (size - 1), coords[1] + 1):
                    if row < 0 or row > self.size:
                        return 1
                    if self.get_box_status([coords[0], row]) in validStates:
                        tempBoard.set_box_status([coords[0], row], Status.ship)
                    else:
                        return 1
            except:
                return 1
        self.board = tempBoard.board
        return 0