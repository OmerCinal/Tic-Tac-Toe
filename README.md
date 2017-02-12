<snippet>
  <content>
# Tic Tac Toe
A modified tic tac toe game both for playing and testing agents that can play the game.
## Installation
1. Create a folder and name it whatever you like
2. Move the Game.py in the folder
## GUI Usage
Load Bots - Loads the agents written in python, which are in the same directory
Setup - Initializes game settings according to selected options
Start - Runs the game once and displays the results
Test - Runs the game the number of times given in the entry box and displays the statistics
Combo boxes - Agents for both players
Board Size - This should be an even number
## Writing your own agent/bot/AI
The code written must be in python and should follow the rules:
- Should include a class. Class name should be the same as the file name
- Init method must have three inputs, first being the empty slot id, second being the player id and third being the opponent id.
Example code:
```python
def __init__(self, empty, me, opponent):
        self.empty = empty
        self.me = me
        self.opponent = opponent
```
- There should also be a play() method. This method will be called by the Game.py at each turn.
This method should have an input as 2D array (nested list), as the current state of the board.
And it should return x, y coordinates as its move.
Example code:
```python
def play(self, board):
        random.seed(self.seed)
        self.seed += 1
        rng = range(len(board))
        slots = []
        for x in rng:
            for y in rng:
                if board[x][y] == self.empty:
                    slots.append((x, y))
        return random.choice(slots)
```
</content>
</snippet>
