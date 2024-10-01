import numpy as np
from grid import Grid
from cell import Cell, Empty_Cell, Shark, Fish
import matplotlib.pyplot as plt
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore, QtWidgets
import random

def create_random_grid_with_probabilities(size, values, probabilities):
    return np.random.choice(values, size=size, p=probabilities)

if __name__ == '__main__':  
    app=pg.mkQApp("WATOR")
    grid_size=(100,100)
    init_values=np.empty(grid_size, dtype=object)# Should be an array of cells. Potentially read from interactive window later.
    values = [Shark(), Fish(), Empty_Cell()]  # The values to spread
    probabilities = [0.1, 0.4, 0.5]  # Probabilities for the values respectively
    grid = create_random_grid_with_probabilities(grid_size, values, probabilities)
    pre_grid=Grid(grid)
    window=QtWidgets.QMainWindow()
    window.resize(1200,600)
    window.setCentralWidget(pre_grid)
    window.show()
    pg.exec()

    # Comment: Perhaps its a bit weird that one shark can go randomly if another shark goes for the fish
    # Perhaps it should stay on the same place then?