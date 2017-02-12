import random, time

class RandomBot:#class name is the same as file name

    def __init__(self, empty, me, opponent):
        self.empty = empty
        self.me = me
        self.opponent = opponent
        self.seed = time.time()

    def play(self, board):#2d array
        random.seed(self.seed)
        self.seed += 1
        rng = range(len(board))
        slots = []
        for x in rng:
            for y in rng:
                if board[x][y] == self.empty:
                    slots.append((x, y))
        return random.choice(slots)

