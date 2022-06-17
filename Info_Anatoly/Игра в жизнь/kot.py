import numpy as np
def life(X, steps):
    """
     Conway's Game of Life.
     - X, matrix with the initial state of the game.
     - steps, number of generations.
    """
    def roll_it(x, y):
        # rolls the matrix X in a given direction
        # x=1, y=0 on the left;  x=-1, y=0 right;
        # x=0, y=1 top; x=0, y=-1 down; x=1, y=1 top left; ...
        return np.roll(np.roll(X, y, axis=0), x, axis=1)
    for _ in range(steps):
        # count the number of neighbours 
        # the universe is considered toroidal
        Y = roll_it(1, 0) + roll_it(0, 1) + roll_it(-1, 0) \
            + roll_it(0, -1) + roll_it(1, 1) + roll_it(-1, -1) \
            + roll_it(1, -1) + roll_it(-1, 1)
        # game of life rules
        X = np.logical_or(np.logical_and(X, Y ==2), Y==3)
        X = X.astype(int)
        yield X
X = np.zeros((40, 40)) 
X[23, 22:24] = 1
X[24, 21:23] = 1
X[25, 22] = 1