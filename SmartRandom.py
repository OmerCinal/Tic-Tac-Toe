import random, time

class SmartRandom:#class name is the same as file name

    def __init__(self, empty, me, opponent):
        self.empty = empty
        self.me = me
        self.opponent = opponent
        self.seed = time.time()


    def play(self, board):
        self.board = board
        random.seed(self.seed)
        self.seed += 1
        
        slots, empties, blocks = self.readboard()
        
        if slots:
            return random.choice(slots)
        
        if blocks:
            return random.choice(blocks)
        
        return random.choice(empties)


    
    def surrounding(self, x, y):
        coords = []
        endx, endy = min(x+2,len(self.board)), min(y+2, len(self.board[0]))
        for i in range(x-1, endx):
            for j in range(y-1, endy):
                if self.board[i][j] == self.empty:
                    coords.append((i, j))
        return coords
        
        
    def readboard(self):
        slots, empties, blocks = [], [], []
        rng = range(len(self.board))
        for x in rng:
            for y in rng:
                
                if self.board[x][y] == self.me:
                    slots.extend(self.surrounding(x, y))
                    
                elif self.board[x][y] == self.opponent:
                    blocks.extend(self.surrounding(x, y))
                    
                else:
                    empties.append((x, y))

        return slots, empties, blocks
