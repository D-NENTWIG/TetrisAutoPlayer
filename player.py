from board import Direction, Rotation, Action, Shape
from random import Random
from time import time


class Player:
    def choose_action(self, board):
        raise NotImplementedError

#Not used
class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def choose_action(self, board):
        if self.random.random() > 0.97:
            # 3% chance we'll discard or drop a bomb
            return self.random.choice([
                Action.Discard,
                Action.Bomb,
            ])
        else:
            # 97% chance we'll make a normal move
            return self.random.choice([
                Direction.Left,
                Direction.Right,
                Direction.Down,
                Rotation.Anticlockwise,
                Rotation.Clockwise,
            ])



#board.falling.left = block min  x coordinate
#board.falling.top = block min y coord
#board.falling.right = block max  x coordinate
#board.falling.bottom = block max y coord

class DavidPlayer(Player):
    def __init__(self, seed=0):
        self.random = Random(seed)

    def choose_action(self, board):    #testing on cloned boards,  GET ALL SCORES APPEND TO LIST CHOOSE HIGHEST SCORE AND USE THAT LIST OF MOVES

        bestmoves = []
        xpos = board.falling.left
        bestscore = -(1 << 30)
        before = 0
        after = 0
        diff = 0
        for x in range(0,10):
            for rot in range(0, 4):
                #print(rot)
                before = self.get_rows_before(board)
                #print("before:" ,before)
                #print("---------------------------------------------")
                clone = board.clone()
                xpos = clone.falling.left
                moves = self.move_toTarget(clone, x, rot, xpos, before)

                after = self.get_rows_after(clone)

                if after < before:
                    diff = (before-after)

                score = self.score_board(clone, diff)
                #print("moves:",moves)
                if score > bestscore:
                    bestscore = score
                    bestmoves = moves
                    #print("bestmoves:",bestmoves)

        return bestmoves
        
        

    def move_toTarget(self, clone, t_x, t_rot, xpos, before):
        
        
        #tested moves
        moves = []
        #rotation
        landed = False
        for rotation in range(t_rot):
            clone.rotate(Rotation.Anticlockwise)
            moves.append(Rotation.Anticlockwise)
            if clone.falling is not None:
                xpos = clone.falling.left
            else:
                landed = True
                break

        #steps
        while xpos > t_x and landed == False:
            clone.move(Direction.Left)
            moves.append(Direction.Left)
            if clone.falling is not None:
                xpos = clone.falling.left
            else:
                landed = True
                break
        while xpos < t_x and landed == False:
            clone.move(Direction.Right)
            moves.append(Direction.Right)
            if clone.falling is not None:
                xpos = clone.falling.left
            else:
                landed = True
                break
        if landed == False:
            clone.move(Direction.Drop)
            moves.append(Direction.Drop)

        return moves


    def score_board(self, board, diff):
        '''
        worse if lower y
        better if lower holes
        return score
        '''

        Ai = 59             #59
        Bi = -16            #-16
        Ci = 0             #10

        A = self.landing_y(board)
        ##print("y:",A)
        #print("scorey:",A*Ai)

        B = self.get_holes(board)
        #print("holes:", B)
        #print("scoreh:",B*Bi)

        C = diff
        if C == 26 or C == 36:
            Ci += 40        #40
        #print("scoreR:",C*Ci)

        D = self.well_heights(board)
        #print("wells:", D)

        score = (Ai*A) + (Bi*B) + (Ci*C)
        #print("score:", score)
        #print("---------------")
        
        return score


    def landing_y(self, board): #Want a low Y, minimal holes, low transitions, and low well heights (unless 3 or 4)
        miny = 24        
        for x,y in board.cells:
            if y < miny:
                miny = y
        return miny
       
    def get_holes(self, board): #Check actual board
        #Get total number of holes
        holes = 0
        for x in range(board.width):
            occupied = False
            for y in range(board.height):
                if (x,y) in board.cells != 0:
                    if not occupied:
                        occupied = True
                elif occupied:
                    holes += 1

        return holes


    def well_heights(self, board):
            #look at how he deals with the coords in board
        wells_height = 0

        for x in range(1, board.width-1):
            for y in range(board.height):
                if (x,y) in board.cells == 0 and {(x-1, y) for (x, y) in board.cells} != 0 \
                        and {(x, y+1) for (x, y) in board.cells} != 0:
                    wells_height += 1
                    for _y in range(y+1, HEIGHT):
                        if {(x, y_) for (x, y) in board.cells} != 0:
                            break
                        wells_height += 1

        for y in range(board.height):
            # check wells in the leftmost boarder of the board
            if {(0, y) for (x, y) in board.cells} == 0 and {(1, y) for (x, y) in board.cells} != 0:
                wells_height += 1
                for _y in range(y+1, board.height):
                    if {(x, y_) for (x, y) in board.cells} != 0:
                        break
                    wells_height += 1

            # check wells in the rightmost border of the board
            if {(board.width - 1, y) for (x, y) in board.cells} == 0 and {(board.width-2, y) for (x, y) in board.cells} != 0:
                wells_height += 1
                for _y in range(y+1, board.height):
                    if {(x, y_) for (x, y) in board.cells} != 0:
                        break
                    wells_height += 1

        return wells_height
    


    #Check cells before and after block placed
    #less cells == more rows cleared
    #maybe dont use fucntion to be faster
    def get_rows_before(self, board):
        
        before_cells = 0

        for y in range (board.height):
            for x in range(board.width):
                if (x,y) in board.cells != 0:
                    before_cells = len(board.cells)
        return before_cells
        
    def get_rows_after(self, board):

        before_cells = 0

        for y in range (board.height):
            for x in range(board.width):
                if (x,y) in board.cells != 0:
                    after_cells = len(board.cells)

        return after_cells

SelectedPlayer = DavidPlayer







        