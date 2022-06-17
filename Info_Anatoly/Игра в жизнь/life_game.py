#Кирюшин Анатолй 8Т
import tkinter
import time
import threading

class gameOfLife:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.makeGrid()        
        self.paused = True
        self.delay = 0.2

        self.gui = GoLGUI(self)

    def clock(self):
        while True:
            if not self.paused:
                self.tick()
            time.sleep(self.delay)

    def toggletick(self):
        self.paused = not self.paused
        if self.paused:
            self.gui.window.wm_title("PAUSED x"+str(self.delay))
        else:
            self.gui.window.wm_title("x"+str(self.delay))
            
    def changeSpeed(self, multiplicand):
        if self.paused:
            if (self.delay * multiplicand) > 0.01 and (self.delay * multiplicand) < 2:
                self.delay *= multiplicand
                if self.paused:
                    self.gui.window.wm_title("PAUSED x"+str(self.delay))
                else:
                    self.gui.window.wm_title("x"+str(self.delay))
    
   # def reset(self):
    #    if self.paused:
     #       self.makeGrid()
      #      for x in range(self.width):
       #         for y in range(self.height):
        #            self.gui.buttonsDict["{0}.{1}".format(x, y)].configure(bg="#FF00FF")
         #   self.gui.window.update()
          #  for x in range(self.width):
           #     for y in range(self.height):
            #        self.gui.buttonsDict["{0}.{1}".format(x, y)].configure(bg="#000000")
            #self.gui.window.update()

    def makeGrid(self):
        self.grid = {x:{y:False for y in range(self.height)} for x in range(self.width)}
        
    def changeState(self, x, y):
        if self.paused:
            self.grid[x][y] = not self.grid[x][y]
            if self.grid[x][y]:
                self.gui.buttonsDict["{0}.{1}".format(x, y)].configure(bg="#FFFFFF")
            else:
                self.gui.buttonsDict["{0}.{1}".format(x, y)].configure(bg="#000000")

    def tick(self):        
        nextGrid = {x:{y:False for y in range(self.height)} for x in range(self.width)}

        for x in range(self.width):
            for y in range(self.height):
                if self.grid.get(x).get(y):
                    nextGrid[x][y] = sum([sum([self.grid.get(xi, {}).get(yi, False) for yi in range(y-1, y+2)]) for xi in range(x-1,x+2)])-1 in [2, 3]
                    if nextGrid[x][y] != self.grid[x][y]:
                        self.gui.buttonsDict["{0}.{1}".format(x, y)].configure(bg="#000000")
                else:
                    nextGrid[x][y] = sum([sum([self.grid.get(xi, {}).get(yi, False) for yi in range(y-1, y+2)]) for xi in range(x-1,x+2)]) == 3
                    if nextGrid[x][y] != self.grid[x][y]:
                        self.gui.buttonsDict["{0}.{1}".format(x, y)].configure(bg="#FFFFFF")

        self.gui.window.update()
        self.grid = nextGrid

class GoLGUI:
    def __init__(self, game):
        self.game = game
        
        self.window = tkinter.Tk()
        self.window.wm_title("PAUSED x"+str(self.game.delay))
        self.window.resizable(False, False)
        self.window.geometry("800x800")

        self.buttonsDict = {}
        
        for x in range(self.game.width):
            self.window.grid_columnconfigure(x, weight=1)
            for y in range(self.game.height):
                self.window.grid_rowconfigure(y, weight=1)
                buttonCmd = self.buttonCmdGen(x, y)
                self.buttonsDict["{0}.{1}".format(x, y)] = tkinter.Label(self.window, bg="#000000")
                self.buttonsDict["{0}.{1}".format(x, y)].grid(row=y, column=x, sticky="nesw")
                self.buttonsDict["{0}.{1}".format(x, y)].bind("<Button-1>", buttonCmd)
        
        self.window.bind("[", lambda a:self.game.changeSpeed(2))
        self.window.bind("]", lambda a:self.game.changeSpeed(0.5))
        
        self.window.bind("<Return>", lambda a:self.game.toggletick())
        self.window.bind("<BackSpace>", lambda a:self.game.reset())
        
    def buttonCmdGen(self, x, y):
        return lambda a: self.game.changeState(x, y)

game = gameOfLife(50, 50)
loop = threading.Thread(target=game.clock)
loop.start()
game.gui.window.mainloop()