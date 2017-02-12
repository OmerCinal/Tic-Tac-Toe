from Tkinter import *
from ttk import Combobox
import os, time, webbrowser


class Game:

    version = "3.7"

    def __init__(self):
        self.root = Tk()
        self.initgui()
        self.gridgui()
        self.configurewidgets()
        self.root.mainloop()

    def initgui(self):
        self.root.title("Tick tack toe")
        self.root.resizable(False, False)
        self.frame_board = Frame(self.root, bg="black")
        self.canvas = Canvas(self.frame_board, width=600, height=600, bg="beige")

        self.frame_options = Frame(self.root)
        self.button_setup = Button(self.frame_options, text="Setup", width=10)
        self.button_start = Button(self.frame_options, text="Start", width=10)
        self.button_reset = Button(self.frame_options, text="Reset", width=10)
        self.button_reload = Button(self.frame_options, text="Load Bots", width=10)
        self.button_test = Button(self.frame_options, text="Test", width=10)

        self.entry_test = Entry(self.frame_options, width=10)

        self.label1 = Label(self.frame_options, text="Player 1")
        self.label2 = Label(self.frame_options, text="Player 2")
        self.combo1 = Combobox(self.frame_options, state="readonly")
        self.combo2 = Combobox(self.frame_options, state="readonly")

        self.entry_shape1 = Entry(self.frame_options, width=5)
        self.entry_shape2 = Entry(self.frame_options, width=5)

        self.label_size = Label(self.frame_options, text="Board Size")
        self.entry_size = Entry(self.frame_options, width=10)
        
        self.label_movements = Label(self.frame_options, text="Steps")
        self.movements = Listbox(self.frame_options, width=25, height=15)

        self.chainVar = 0
        self.button_chain = Button(self.frame_options, text="Show Chains", width=10)

        self.button_help = Button(self.frame_options, text="?", width=3)
        self.label_version = Label(self.frame_options, text="Version v"+self.version)
        

    def gridgui(self):
        self.frame_board.grid(row=0, column=0, padx=5, pady=5)
        self.canvas.grid(padx=5, pady=5)

        self.frame_options.grid(row=0, column=1, padx=5, pady=5)
        self.button_reload.grid(pady=5, columnspan=2)
        self.button_setup.grid(pady=5, columnspan=2)
        self.button_start.grid(pady=5, columnspan=2)
        self.button_test.grid(row=3, column=0, pady=5)
        self.entry_test.grid(row=3, column=1, pady=5)
        
        self.label1.grid(row=4, column=0, stick=W, pady=5)
        self.entry_shape1.grid(row=4, column=1)
        self.combo1.grid(stick=W, pady=5, columnspan=2)
        self.label2.grid(row=6, column=0, stick=W, pady=5)
        self.entry_shape2.grid(row=6, column=1)
        self.combo2.grid(stick=W, pady=5, columnspan=2)

        self.label_size.grid(row=8, stick=W, pady=5, columnspan=2)
        self.entry_size.grid(row=8, stick=E, pady=5, columnspan=2)

        self.button_chain.grid(columnspan=2)

        self.button_reset.grid(columnspan=2)

        self.label_movements.grid(columnspan=2)
        self.movements.grid(columnspan=2)
        self.label_version.grid(row=14, column=0, pady=5)
        self.button_help.grid(row=14, column=1, pady=5)


    def configurewidgets(self):
        self.reset(None)
        
        self.button_reload.bind("<ButtonRelease-1>", self.reloadbots)
        self.button_reset.bind("<ButtonRelease-1>", self.reset)
        self.button_chain.bind("<ButtonRelease-1>", self.drawChains)
        self.button_help.bind("<ButtonRelease-1>", self.helpGit)


    def helpGit(self, event):
        webbrowser.open("https://github.com/OmerCinal/Tic-Tac-Toe")


    def reloadbots(self, event):
        path = os.path.dirname(os.path.realpath(__file__))
        files = [f.split(".")[0] for f in os.listdir(path) if (os.path.isfile(path +"/"+ f) and (f.split(".")[-1] == "py"))]

        if "Game" in files:
            files.remove("Game")
        
        self.modules = dict(map((lambda x: (x.__name__, x)), map(__import__, files)))

        self.combo1["values"] = self.modules.keys()
        self.combo2["values"] = self.modules.keys()
        self.combo1.current(0)
        self.combo2.current(0)

        self.updateButtons()

    
    def setup(self, event):
        if not hasattr(self, "modules"):
            self.root.bell()
            return
        error = ""
        try:
            self.player1 = getattr(self.modules[self.combo1.get()], self.combo1.get())(0,1,2)
        except:
            error += " 1 "

        try:
            self.player2 = getattr(self.modules[self.combo2.get()], self.combo2.get())(0,2,1)
        except:
            error += " 2 "

        if error:
            self.message("Error with the following players:" + error)
            return
            
        self.size = self.validateSize(self.entry_size.get())
        self.movements.delete(0, END)
        
        if not self.size:
            self.message("Board size cannot contain letters\nand it must be an even number")
            return

        self.drawboard(self.size)
        self.board = [ [0]*self.size for _ in range(self.size) ]
        self.updateButtons()


    def drawboard(self, n):
        space = 50
        start = (space*3)/2
        board = self.canvas
        board.delete(ALL)

        for i in range(n):
            board.create_text(space*(i+2), space, text=str(i), anchor=W, tag="coord", font=50)
            board.create_text(space, space*(i+2), text=str(i), anchor=W, tag="coord", font=50)
            
        for i in range(n+1):
            board.create_line(start, start + space*i, start + space*n, start + space*i, tag="line", width=2.0, fill="goldenrod")
            board.create_line(start + space*i, start, start + space*i, start + space*n, tag="line", width=2.0, fill="goldenrod")


    def start(self, event):
        if not hasattr(self, "board"):
            self.message("Please Set the game first")
            return
        self.board = [ [0]*self.size for _ in range(self.size) ]
        shape1 = self.entry_shape1.get()
        shape2 = self.entry_shape2.get()
        score1, score2, steps = self.playOnce(shape1, shape2, self.player1, self.player2, record=True)
        self.drawboard(self.size)
        self.updateboard(shape1, shape2)

        self.movements.delete(0, END)
        for step in steps:
            self.movements.insert(END, step)

        self.canvas.create_text(300, 25, text="".join((shape1,": ",str(score1),";  ",shape2,": ",str(score2))) )
        

    def test(self, event):
        if not hasattr(self, "board"):
            self.message("Please Set the game first")
            return
        
        shape1 = self.entry_shape1.get()
        shape2 = self.entry_shape2.get()
        
        try:
            testrange = self.validateInt(self.entry_test.get())
        except:
            self.message("Number of tests can only be integers")
            return
        
        clear = self.canvas.delete
        write = self.canvas.create_text
        update = self.canvas.update
        scores1 = [0]*testrange
        scores2 = [0]*testrange
        turn = True
        
        for step in range(testrange):
            self.board = [ [0]*self.size for _ in xrange(self.size) ]
            if turn:
                scores1[step], scores2[step] = self.playOnce(shape1, shape2, self.player1, self.player2)
                turn = False
            else:
                scores2[step], scores1[step] = self.playOnce(shape1, shape2, self.player2, self.player1)
                turn = True

            if step % 10 == 0:
                clear(ALL)
                write(300, 100, text="".join(("Games played: %", str((step*100.0)/testrange))), font=50)
                update()

        avg1 = sum(scores1)/len(scores1)
        avg2 = sum(scores2)/len(scores2)
        wins1, wins2, ties = 0, 0, 0

        for p1, p2 in zip(scores1, scores2):
            if p1 > p2:
                wins1 += 1
            elif p1 < p2:
                wins2 += 1
            else:
                ties += 1
                
        result = ["Results:",
                  "",
                  "Player:\t"+shape1+",\t"+shape2,
                  "Wins:  \t"+str(wins1)+",\t"+str(wins2),
                  "Avg:   \t"+str(avg1)+",\t"+str(avg2),
                  "Ties:  \t"+str(ties),
                  "",
                  "Winner: "+(shape1 if wins1 > wins2 else shape2)]
        
        self.canvas.delete(ALL)
        self.canvas.create_text(100, 100, text="\n".join(result), anchor=W, font=50)


    def playOnce(self, shape1, shape2, player1, player2, record=False, human=False):
        play1 = player1.play
        play2 = player2.play

        if record:
            step = 1
            steps = []
        while not self.endgame():
            x1, y1 = play1(self.board)
            self.board[x1][y1] = 1

            x2, y2 = play2(self.board)
            self.board[x2][y2] = 2

            if human:
                self.updateboard(shape1, shape2)
                
            if record:
                steps.append("".join((str(step),"- ",shape1, ": (", str(x1), ", ", str(y1), "); ",shape2, ": (", str(x2), ", ", str(y2), ")")))
                step += 1
            
        s1,s2 = self.getScores(1, 2)
        if record:
            return s1, s2, steps
        return s1, s2
        


    def updateboard(self, shape1, shape2):
        write = self.canvas.create_text
        rng = range(self.size)
        space = 50
        self.canvas.delete("shape")
        
        for x in rng:
            for y in rng:
                if self.board[x][y] == 1:
                    write(space*(y+2), space*(x+2), text=shape1, tags=("shape1","shape"), font=("Times",20,"bold"))
                elif self.board[x][y] == 2:
                    write(space*(y+2), space*(x+2), text=shape2, tags=("shape2","shape"), font=("Times",20,"bold"))



    def reset(self, event):
        self.canvas.delete(ALL)
        if hasattr(self, "modules"): del self.modules
        if hasattr(self, "board"): del self.board
        self.combo1["values"] = ("None")
        self.combo2["values"] = ("None")
        self.combo1.current(0)
        self.combo2.current(0)
        self.entry_size.delete(0, END)
        self.entry_test.delete(0, END)
        self.entry_shape1.delete(0, END)
        self.entry_shape2.delete(0, END)
        self.entry_size.insert(END, "10")
        self.entry_shape1.insert(END, "X")
        self.entry_shape2.insert(END, "O")
        self.entry_test.insert(END, "1000")
        self.movements.delete(0, END)
        
        msg="""
        Tic Tac Toe
        
        1-Load the bots inside the directory by pressing "Load Bots"
        2-Configure the game and press "Setup"
        3-"Start" for one game
          "Test" for # of games

        Click the question mark for more information
        """
        self.canvas.create_text(100, 100, text=msg, font=100, anchor=W)

        self.updateButtons()


    def message(self, msg):
        self.canvas.delete(ALL)
        self.canvas.create_text(300, 100, text=msg, font=20)
        self.root.bell()


    def updateButtons(self):
        if hasattr(self, "modules"):
            self.button_setup["state"] = NORMAL
            self.button_setup.bind("<ButtonRelease-1>", self.setup)
        else:
            self.button_setup["state"] = DISABLED
            self.button_setup.unbind("<ButtonRelease-1>")
        if hasattr(self, "board"):
            self.button_start["state"] = NORMAL
            self.button_test["state"] = NORMAL
            self.button_start.bind("<ButtonRelease-1>", self.start)
            self.button_test.bind("<ButtonRelease-1>", self.test)
        else:
            self.button_start["state"] = DISABLED
            self.button_test["state"] = DISABLED
            self.button_start.unbind("<ButtonRelease-1>")
            self.button_test.unbind("<ButtonRelease-1>")
    
        

    def getScores(self, p1, p2):

        def getHorizontal(x, y, p):
            x1, x2 = x, x
            while x1 > 0:
                if self.board[x1-1][y] == p:
                    x1 -= 1
                else:
                    break

            while x2 < self.size-1:
                if self.board[x2+1][y] == p:
                    x2 += 1
                else:
                    break

            return (x1,y,x2,y) if (x2 - x1) > 1 else 0
                
                
        def getVertical(x, y, p):
            y1, y2 = y, y
            while y1 > 0:
                if self.board[x][y1-1] == p:
                    y1 -= 1
                else:
                    break

            while y2 < self.size-1:
                if self.board[x][y2+1] == p:
                    y2 += 1
                else:
                    break

            return (x,y1,x,y2) if (y2 - y1) > 1 else 0


        def getDiagonal1(x, y, p):
            x1, y1, x2, y2 = x, y, x, y
            while x1 > 0 and y1 > 0:
                if self.board[x1-1][y1-1] == p:
                    x1 -= 1
                    y1 -= 1
                else:
                    break

            while x2 < self.size-1 and y2 < self.size-1:
                if self.board[x2+1][y2+1] == p:
                    x2 += 1
                    y2 += 1
                else:
                    break

            return (x1,y1,x2,y2) if ((x2-x1 > 1) or (y2-y1 > 1)) else 0

        def getDiagonal2(x, y, p):
            x1, y1, x2, y2 = x, y, x, y
            while x1 < self.size-1 and y1 > 0:
                if self.board[x1+1][y1-1] == p:
                    x1 += 1
                    y1 -= 1
                else:
                    break

            while x2 > 0 and y2 < self.size-1:
                if self.board[x2-1][y2+1] == p:
                    x2 -= 1
                    y2 += 1
                else:
                    break

            return (x1,y1,x2,y2) if ((x2-x1 > 1) or (y2-y1 > 1)) else 0


        self.chains = {p1:[], p2:[]} #p:[ (x1,y1,x2,y2) ]
        rng = range(len(self.board))

        for x in rng:
            for y in rng:
                player = self.board[x][y]

                hor = getHorizontal(x, y, player)
                ver = getVertical(x, y, player)
                crs1 = getDiagonal1(x, y, player)
                crs2 = getDiagonal2(x, y, player)

                self.chains[player].extend(filter((lambda x: x and (x not in self.chains[player])), [hor, ver, crs1, crs2]))
        
        scores = {p1:0, p2:0}

        for player in self.chains:
            for chain in self.chains[player]:
                length = max(chain[2] - chain[0], chain[3] - chain[1]) + 1
                scores[player] += sum(range(3, length+1))

        return scores[p1], scores[p2]


    def drawChains(self, event):
        if self.canvas.find_withtag("chain"):
            self.canvas.delete("chain")
            return
        if not self.canvas.find_withtag("shape") or not hasattr(self, "chains"):
            return
        space = 50
        start = 2*space
        colors = {1:"red",2:"blue"}
        for p in self.chains:
            for x1, y1, x2, y2 in self.chains[p]:
                self.canvas.create_line(start+y1*space, start+x1*space, start+y2*space ,start+x2*space, fill=colors[p], tag="chain", state=NORMAL, width=5.0)
        

    def endgame(self):
        rng = range(len(self.board))
        for x in rng:
            for y in rng:
                if self.board[x][y] == 0:
                    return False
        return True
    

    @staticmethod
    def validateSize(val):
        try:
            if int(val) % 2 == 0:
                return int(val)
            return False
        except:
            return False


    @staticmethod
    def validateInt(val):
        try:
            return int(val)
        except:
            return False


    
        


def main():
    game = Game()

if __name__ == "__main__":
    main()
