<snippet>
  <content>
# Tic Tac Toe
A modified tic tac toe game for testing agents that can play the game.

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

## Game rules

- The are 2 players; X and O.

- Players should make chains of 3 and more. Horizontal, vertical and diagonal.

- Longer chains give more points. For every length of chain, the score is calculated by sum(range(3, length+1)):

The code that calculates the score:

```python
# gets chain length from coordiantes 
length = max(x2 - x1, y2 - y1) + 1
# increases the total score  
score += sum(range(3, length+1))
```
for 3 the score is 3

for 4 the score is 3 + 4 = 7

for 5 the score is 3 + 4 + 5 = 12

for 6 the score is 3 + 4 + 5 + 6 = 18

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
		# board will be updated by the game
		self.board = []
```

- There should also be a play() method. This method will be called by the Game.py at each turn.
It should return x, y coordinates as its next move.

Example code:
```python
def play(self): # Randomized Bot
        # Make sure the result is random
        random.seed(self.seed)
        self.seed += 1
        
        # Create a range
        rng = range(len(self.board))
        # A list for empty slots
        slots = []
        for x in rng:
            for y in rng:
                if self.board[x][y] == self.empty:
                    slots.append((x, y))
        
        # Return a random choice from the list of empty slots
        return random.choice(slots)
```
When you are done, move your code to Game.pyw folder. 

You can use the RandomBot.py as a template.
</content>
</snippet>
