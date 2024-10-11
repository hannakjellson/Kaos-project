import numpy as np
from grid import Grid
from cell import Cell, Empty_Cell, Shark, Fish, Crill, Algae
import matplotlib.pyplot as plt
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore, QtWidgets
import random

def create_random_grid_with_probabilities(size, values, probabilities):
    return np.array([[random.choices(values, probabilities)[0]() for _ in range(size[0])] for _ in range(size[1])])

if __name__ == '__main__':  
    # app=pg.mkQApp("WATOR")
    random.seed(2)
    np.random.seed(2)
    grid_size=(100,100)
    init_values=np.empty(grid_size, dtype=object) # Should be an array of cells. Potentially read from interactive window later.
    values = [Crill, Algae, Shark, Fish, Empty_Cell] # The values to spread
    probabilities = [0.20, 0.20, 0.20, 0.20, 0.20]  # Probabilities for the values respectively
    grid = create_random_grid_with_probabilities(grid_size, values, probabilities)
    pre_grid=Grid(grid, allow_escape=True)
    # window=QtWidgets.QMainWindow()
    # window.resize(1200,600)
    # window.setCentralWidget(pre_grid)
    # window.show()
    # pg.exec()
    for i in range(10):
        pre_grid.update()
    plt.figure()
    algae_nbrs, crill_nbrs, fish_nbrs, shark_nbrs=pre_grid.get_numbers()
    plt.plot(algae_nbrs, label='Algae')
    plt.plot(crill_nbrs, label='Crill')
    plt.plot(fish_nbrs, label='Fish')
    plt.plot(shark_nbrs, label='Shark')
    plt.legend()
    plt.show()

    # Comment: Perhaps its a bit weird that one shark can go randomly if another shark goes for the fish
    # Perhaps it should stay on the same place then?
    # TODO: var tionde gång en haj äter, förökar den sig, var tionde steg den tar dör den.
    # Allt ska föröka sig men bara hajen dör av ålder, eventuellt också krill och fisk.