import numpy as np
import random
from cell import Cell, Empty_Cell, Fish, Shark, Algae, Crill
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore, QtWidgets
import matplotlib.pyplot as plt
# QtWidgets.QWidget
# TODO: They can lay eggs instead. Try to make the births match what is in lotka volterra, remember that we have andelar in Lotka. Perhaps reset the algae thing. Note that the initial conditions in Lotka are very small. How to handle in this model?
class Grid():
    def __init__(self, array, allow_escape=None):
        """
        Initialize the grid
        size: int
        array: numpy.ndarray with Cell elements
        """
        super().__init__()
        self.size=np.shape(array)
        self.array=array
        # self.day=QtCore.QTimer()
        # self.day.timeout.connect(self.update)
        # self.day.start(10)
        self.algae_nbrs=[]
        self.crill_nbrs=[]
        self.fish_nbrs=[]
        self.shark_nbrs=[]
        self.allow_escape=False if allow_escape is None else allow_escape

    def __getitem__(self, cell_id):
        """
        Allows for getting an element in the grid using grid[i,j]
        cell_id: tuple
        """
        i,j=cell_id
        return self.array[i][j]

    def get_matrix(self):
        """
        Return the grid as a numpy.ndarray 
        """
        return self.array
    
    def get_center(self):
        """
        Return the index of the center cell, in case of using other grids than squares.
        """
        # TODO generalize for other shapes. This works now as it is only called for 3x3 grids.
        return (1,1)      
    
    def get_local_species(self, cell_id):
        """
        Return the Cell at cell_id and its neighbours.
        cell_id: tuple
        """
        # TODO: make it work at borders
        row_indices=[cell_id[0]-1, cell_id[0], (cell_id[0]+1) % self.size[0]]
        col_indices=[cell_id[1]-1, cell_id[1], (cell_id[1]+1) % self.size[1]]
        
        return Grid(self.array[np.ix_(row_indices, col_indices)])
    
    def set_local_species(self, cell_id, local_species):
        """
        Update the Cell at cell_id and its neighbours such that they have the values in local_species
        cell_id: tuple
        cell_id: tuple
        local_species: Grid
        """
        row_indices=[cell_id[0]-1, cell_id[0], (cell_id[0]+1) % self.size[0]]
        col_indices=[cell_id[1]-1, cell_id[1], (cell_id[1]+1) % self.size[1]]
        self.array[np.ix_(row_indices, col_indices)]=local_species.get_matrix()


    def set_specie(self, cell_id, specie):
        """
        Updates the specie at position cell_id to specie.
        cell_id: tuple
        """
        self.array[cell_id]=specie
    
    def where_none(self):
        is_none=np.vectorize(lambda cell: isinstance(cell, Empty_Cell))
        return is_none(self.array)

    def where_algae(self):
        is_algae=np.vectorize(lambda cell: isinstance(cell, Algae))
        return is_algae(self.array)
    
    def where_crill(self):
        is_crill=np.vectorize(lambda cell: isinstance(cell, Crill))
        return is_crill(self.array)
    
    def where_fish(self):
        is_fish=np.vectorize(lambda cell: isinstance(cell, Fish))
        return is_fish(self.array)
    
    def where_shark(self):
        is_shark=np.vectorize(lambda cell: isinstance(cell, Shark))
        return is_shark(self.array)

    def get_none_indices(self):
        """
        Returns all indices where the grid has Empty_Cells.
        """
        none_indices=np.argwhere(self.where_none())
        none_indices=[tuple(none_index) for none_index in none_indices]
        return none_indices
    
    def get_algae_indices(self):
        algae_indices=np.argwhere(self.where_algae())
        algae_indices=[tuple(algae_index) for algae_index in algae_indices]
        return algae_indices
    
    def get_crill_indices(self):
        crill_indices=np.argwhere(self.where_crill())
        crill_indices=[tuple(crill_index) for crill_index in crill_indices]
        return crill_indices
    
    def get_fish_indices(self):
        fish_indices=np.argwhere(self.where_fish())
        fish_indices=[tuple(fish_index) for fish_index in fish_indices]
        return fish_indices
    
    def get_shark_indices(self):
        shark_indices=np.argwhere(self.where_shark())
        shark_indices=[tuple(shark_index) for shark_index in shark_indices]
        return shark_indices
        
    def get_common_none_indices(self, other_grid):
        """
        Returns indices where both self and other grids have Empty_Cells
        other_grid: Grid with the same size as self.
        """
        common_none_indices = np.argwhere(np.logical_and(self.where_none(), other_grid.where_none()))
        common_none_indices=[tuple(common_none_index) for common_none_index in common_none_indices]
        return common_none_indices


    def get_random_common_none_index(self, other_grid, size):
        # Randomly pick an index from the common None indices
        common_none_indices=self.get_common_none_indices(other_grid)
        if common_none_indices:
            return random.choice(common_none_indices) if size==1 else random.sample(common_none_indices, size)
        else:
            return None  # Return None if no common None indices are found
        
    def get_species(self):
        algaes=self.array[self.where_algae()]
        crills=self.array[self.where_crill()]
        fish=self.array[self.where_fish()]
        sharks=self.array[self.where_shark()]
        return len(algaes), len(crills), len(fish), len(sharks)
    
    def get_numbers(self):
        return (self.algae_nbrs, self.crill_nbrs, self.fish_nbrs, self.shark_nbrs)
    
    def update(self):
        """
        Updates the grid
        """

        # Split up indices in different species
        algae_indices=self.get_algae_indices()
        shark_indices=self.get_shark_indices()
        fish_indices=self.get_fish_indices()
        crill_indices=self.get_crill_indices()

        other_species_indices=shark_indices+fish_indices+crill_indices
        if self.allow_escape:
            # Randomize order in which they are updates s.t. fish and crill can escape. Algae can not escape.
            np.random.shuffle(other_species_indices) 

        not_none_indices=algae_indices+other_species_indices

        # Creating arrays. 
        empty_array=np.empty(self.size, dtype=object)
        empty_array[empty_array==None]=Empty_Cell() 
        moved_species_grid=Grid(empty_array)

        # Setting priorities. Probably only necessary if we allow escapes
        for i, index in enumerate(not_none_indices):
            self.array[index].set_priority(i)
    
        # For keeping track of how many new eggs have been layn. If a species does not lay egg, this remains zero.
        num_crill_meals=0
        num_fish_meals=0
        num_shark_meals=0

        # Looping through all species.
        for index in not_none_indices:
            # Getting local and moved local species
            i,j=index
            local_species=self.get_local_species(index)
            moved_local_species=moved_species_grid.get_local_species(index)

            # Updating Cell and moved species grid
            updated_moved_local_species=self.array[i][j].update(local_species, moved_local_species)
            moved_species_grid.set_local_species(index, updated_moved_local_species)

            # Updating the number of kids
            current_specie=self.array[index]
            if (not isinstance(current_specie, Algae)) and current_specie.had_meal and current_specie.lay_egg:
                if isinstance(current_specie, Crill):
                    num_crill_meals+=1
                elif isinstance(current_specie, Fish):
                    num_fish_meals+=1
                elif isinstance(current_specie, Shark):
                    num_shark_meals+=1

        # Add new species and algae at random
        algae_nbr, _, _, _=self.get_species()
        num_new_algae=int(algae_nbr*0.8)
        num_new_crill=int(num_crill_meals*4/3)
        num_new_fish=int(num_fish_meals*1/2)
        num_new_shark=int(num_shark_meals)
        new_species=[Shark(0,0,False) for i in range(num_new_shark)]+[Fish(0,0,False) for i in range(num_new_fish)]+ [Crill(0,0,False) for i in range(num_new_crill)]+[Algae() for i in range(num_new_algae)]
        random.shuffle(new_species)
        none_indices=moved_species_grid.get_none_indices() # Could also do this with common none indices, depends on if we allow things to pop up where something just left.
        nbr_of_places=len(none_indices) if len(none_indices)<len(new_species) else len(new_species)
        new_kid_indices=random.sample(none_indices, nbr_of_places)
        for i, index in enumerate(new_kid_indices):
            moved_species_grid.set_specie(index, new_species[i])

        # Update the matrix
        # print(moved_species_grid.get_none_indices())
        self.array=moved_species_grid.get_matrix()

        # Keeping track of the number of each species
        algae_nbr, crill_nbr, fish_nbr, shark_nbr=self.get_species()
        self.algae_nbrs.append(algae_nbr)
        self.crill_nbrs.append(crill_nbr)
        self.fish_nbrs.append(fish_nbr)
        self.shark_nbrs.append(shark_nbr)

        # Repainting
        # self.repaint()

    # def paintEvent(self, e):
    #     painter = QtGui.QPainter(self)
    #     brush = QtGui.QBrush()
    #     brush.setColor(QtGui.QColor('black'))
    #     brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
    #     rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
    #     painter.fillRect(rect, brush)
    #     painter.setPen(QtGui.QPen(QtGui.QColor(150, 150, 150), 1))
    #     cells = [[QtGui.QPainterPath() for j in range(self.size[1])] for i in
    #              range(self.size[0])]  # Path är lätt att göra customizable
    #     dx = self.width() / len(cells)
    #     dy = self.height() / len(cells[0])
    #     for i in range(len(cells)):
    #         for j in range(len(cells[0])):
    #             x0 = i * dx
    #             y0 = j * dy
    #             cells[i][j].moveTo(x0, y0)
    #             cells[i][j].lineTo(x0, y0 + dy)
    #             cells[i][j].lineTo(x0 + dx, y0 + dy)
    #             cells[i][j].lineTo(x0 + dx, y0)
    #             cells[i][j].lineTo(x0, y0)
    #             color=self.array[i][j].getColor()
    #             brush.setColor(QtGui.QColor(color[0], color[1], color[2]))
    #             painter.setBrush(brush)  # Sätter till en kopia av brush, har inte pointern till brush
    #             painter.drawPath(cells[i][j])