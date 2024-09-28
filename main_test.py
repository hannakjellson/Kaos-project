import numpy as np
from grid import Grid
from cell import Cell, Empty_Cell, Shark, Fish
import matplotlib.pyplot as plt

if __name__ == '__main__':  
    grid_size=(10,10)
    init_values=np.empty(grid_size, dtype=object)# Should be an array of cells. Potentially read from interactive window later.
    init_values[5,5]=Shark()
    init_values[7,3]=Fish()
    init_values[7,4]=Shark()
    init_values[7,2]=Shark()
    init_values[init_values == None]=Empty_Cell()
    pre_grid=Grid(init_values)
    vectorized_specie=np.vectorize(lambda cell: cell.get_specie())
    plt.figure()
    plottable_grid=vectorized_specie(init_values)
    plottable_grid[plottable_grid == None]=0
    plottable_grid=plottable_grid.astype(int)
    plt.imshow(plottable_grid)
    plt.show()
    for i in range(5):
        pre_grid.update()
        # TODO: plot using the already created plotting stuff.
        plottable_grid=vectorized_specie(pre_grid.get_matrix())
        plottable_grid[plottable_grid == None]=0
        plottable_grid=plottable_grid.astype(int)
        plt.imshow(plottable_grid)
        plt.show()
        
    # Comment: Perhaps its a bit weird that one shark can go randomly if another shark goes for the fish
    # Perhaps it should stay on the same place then?