import numpy as np
import random
from cell import Cell, Empty_Cell, Fish, Shark, Algae, Crill
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore, QtWidgets


class Grid(QtWidgets.QWidget):
    def __init__(self, array):
        """
        Initialize the grid
        size: int
        array: numpy.ndarray with Cell elements
        """
        super().__init__()
        self.size=np.shape(array)
        self.array=array
        self.day=QtCore.QTimer()
        self.day.timeout.connect(self.update)
        self.day.start(40)

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
        # TODO: make it work at borders
        row_indices=[cell_id[0]-1, cell_id[0], (cell_id[0]+1) % self.size[0]]
        col_indices=[cell_id[1]-1, cell_id[1], (cell_id[1]+1) % self.size[1]]
        self.array[np.ix_(row_indices, col_indices)]=local_species.get_matrix()


    def set_specie(self, cell_id, specie):
        """
        Updates the specie at position cell_id to specie.
        cell_id: tuple
        """
        self.array[cell_id]=specie

    def __is_none(self, cell_id):
        """
        Checks whether the Cell at cell_id is an Empty_Cell
        cell_id: tuple
        """
        return isinstance(self.array[cell_id[0]][cell_id[1]], Empty_Cell)

    def get_none_indices(self):
        """
        Returns all indices where the grid has Empty_Cells.
        """
        none_indices = []
        for i, row in enumerate(self.array):
            for j, element in enumerate(row):
                if self.__is_none((i,j)):
                    none_indices.append((i, j))
        return none_indices
    
    def get_algae_indices(self):
        algae_indices = []
        for i, row in enumerate(self.array):
            for j, element in enumerate(row):
                if isinstance(self.array[i,j], Algae):
                    algae_indices.append((i, j))
        return algae_indices
    
    def get_random_common_none_index(self, other_grid):
        """
        Returns indices where both self and other grids have Empty_Cells
        other_grid: Grid with the same size as self.
        """
        common_none_indices = []

        # Loop through all indices to find where both matrices have None
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                cell_id=(i,j)
                if self.__is_none(cell_id) and other_grid.__is_none(cell_id):
                    common_none_indices.append((i, j))

        # Randomly pick an index from the common None indices
        if common_none_indices:
            return random.choice(common_none_indices)
        else:
            return None  # Return None if no common None indices are found
    
    def update(self):
        """
        Updates the grid
        """
        indices = [(i, j) for i in range(self.size[0]) for j in range(self.size[1])]

        # Split up indices in None indices and other indices.
        none_indices=self.get_none_indices()
        algae_indices=self.get_algae_indices()
        other_species_indices=[element for element in indices if element not in none_indices and element not in algae_indices]

        # Randomize priority. Idea: choose priority rules based on how long they have gone without food and age.
        # Might not be good to observe chaos.
        np.random.shuffle(other_species_indices) 
        not_none_indices=np.vstack((algae_indices, other_species_indices))

        # Creating arrays. 
        # Can probably be written nicer. It's a bit messy with Cells and Grids, but I guess it is good if we want to add more info?
        empty_array=np.empty(self.size, dtype=object)
        empty_array[empty_array==None]=Empty_Cell() 
        moved_species_grid=Grid(empty_array)

        # Looping through all species.
        for index in not_none_indices:
            # Getting local and moved local species
            i,j=index
            local_species=self.get_local_species(index)
            moved_local_species=moved_species_grid.get_local_species(index)

            # Updating Cell and moved species grid
            updated_moved_local_species=self.array[i][j].update(local_species, moved_local_species)
            moved_species_grid.set_local_species(index, updated_moved_local_species)

        self.array=moved_species_grid.get_matrix()
        self.repaint()

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor('black'))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)
        painter.setPen(QtGui.QPen(QtGui.QColor(150, 150, 150), 1))
        cells = [[QtGui.QPainterPath() for j in range(self.size[1])] for i in
                 range(self.size[0])]  # Path är lätt att göra customizable
        dx = self.width() / len(cells)
        dy = self.height() / len(cells[0])
        for i in range(len(cells)):
            for j in range(len(cells[0])):
                x0 = i * dx
                y0 = j * dy
                cells[i][j].moveTo(x0, y0)
                cells[i][j].lineTo(x0, y0 + dy)
                cells[i][j].lineTo(x0 + dx, y0 + dy)
                cells[i][j].lineTo(x0 + dx, y0)
                cells[i][j].lineTo(x0, y0)
                color=self.array[i][j].getColor()
                brush.setColor(QtGui.QColor(color[0], color[1], color[2]))
                painter.setBrush(brush)  # Sätter till en kopia av brush, har inte pointern till brush
                painter.drawPath(cells[i][j])