import numpy as np
from grid import Grid
from cell import Cell, Empty_Cell, Shark, Fish

if __name__ == '__main__':  
    grid_size=(10,10)
    init_values=np.empty(grid_size, dtype=object)# Should be an array of cells. Potentially read from interactive window later.
    init_values[5,5]=Shark(False)
    init_values[1,3]=Fish(False)
    init_values[init_values == None]=Empty_Cell()
    pre_grid=Grid(init_values)
    pre_grid.update()
    print(pre_grid.get_matrix())