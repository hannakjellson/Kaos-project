import numpy as np
from grid import Grid
from cell import Cell, Empty_Cell, Shark, Fish, Crill, Algae
import numpy as np
from grid import Grid
from cell import Cell, Empty_Cell, Shark, Fish, Crill, Algae
import matplotlib.pyplot as plt
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore, QtWidgets
import random

def create_random_grid_with_probabilities(size, values, probabilities, max_ages=[50, 50, 50], lay_egg=False, meals_for_birth=[1, 1, 1], separate_gender=False):
    def create_instance(value):
        """Helper function to create instances of the objects, with arguments where necessary."""
        if value == Shark:
            return Shark(max_age=max_ages[0], lay_egg=lay_egg, meals_for_birth=meals_for_birth[0], separate_gender=separate_gender)
        if value == Fish:
            return Fish(max_age=max_ages[1], lay_egg=lay_egg, meals_for_birth=meals_for_birth[1], separate_gender=separate_gender)
        if value == Crill:
            return Crill(max_age=max_ages[2], lay_egg=lay_egg, meals_for_birth=meals_for_birth[2], separate_gender=separate_gender)     
        return value()  
        
    return np.array([
        [create_instance(random.choices(values, probabilities)[0]) for _ in range(size[0])]
        for _ in range(size[1])
    ])

if __name__ == '__main__':  
    app=pg.mkQApp("WATOR")
    random.seed(3)
    np.random.seed(3)

    grid_size=(100,100)
    init_values=np.empty(grid_size, dtype=object) # Should be an array of cells. Potentially read from interactive window later.
    values = [Crill, Algae, Shark, Fish, Empty_Cell] # The values to spread

    # Gives nice periodic solution. Yet to find......
    probabilities = [0.2, 0.2, 0.01, 0.2, 0.29]
    max_ages=[10, 30, 100]
    lay_egg=False
    meals_for_birth=[1,2,1]
    separate_gender=True
    algae_probability=0.2
    meal_to_children=[0,0,0]

    # # Gives chaos. Note that I have changed such that a kid will always be born before an algae is created.
    # random.seed(2)
    # np.random.seed(2)
    # probabilities = [0.20, 0.20, 0.20, 0.20, 0.20]  # Probabilities for the values respectively
    # max_ages=[5,100,100]
    # lay_egg=True
    # meals_for_birth=[0,0,0]
    # separate_gender=False
    # algae_probability=0.8
    # meal_to_children=[1, 1/2, 4/3]

    # Create grid
    grid = create_random_grid_with_probabilities(grid_size, values, probabilities, max_ages=max_ages, lay_egg=lay_egg, meals_for_birth=meals_for_birth, separate_gender=separate_gender)
    pre_grid=Grid(grid, allow_escape=True, algae_probability=algae_probability, meal_to_children=meal_to_children, max_ages=max_ages, lay_egg=lay_egg, meals_for_birth=meals_for_birth, separate_gender=separate_gender)
    window=QtWidgets.QMainWindow()
    window.resize(1200,600)
    window.setCentralWidget(pre_grid)
    window.show()
    pg.exec()
    # for i in range(10):
    #     pre_grid.update()
    # plt.figure()
    algae_nbrs, crill_nbrs, fish_nbrs, shark_nbrs=pre_grid.get_numbers()
    plt.plot(algae_nbrs, label='Algae')
    plt.plot(crill_nbrs, label='Crill')
    plt.plot(fish_nbrs, label='Fish')
    plt.plot(shark_nbrs, label='Shark')
    plt.legend()
    plt.show()

    # Comment: Perhaps its a bit weird that one shark can go randomly if another shark goes for the fish
    # Perhaps it should stay on the same place then?