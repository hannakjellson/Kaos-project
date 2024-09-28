import numpy as np
import random
from cell import Cell, Empty_Cell, Fish, Shark


class Grid():
    def __init__(self, array):
        """
        Initialize the grid
        size: int
        array: numpy.ndarray with Cell elements
        """
        self.size=np.shape(array)
        self.array=array

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
        return Grid(self.array[cell_id[0]-1:cell_id[0]+2,cell_id[1]-1:cell_id[1]+2])
    
    def set_local_species(self, cell_id, local_species):
        """
        Update the Cell at cell_id and its neighbours such that they have the values in local_species
        cell_id: tuple
        cell_id: tuple
        local_species: Grid
        """
        # TODO: make it work at borders
        self.array[cell_id[0]-1:cell_id[0]+2,cell_id[1]-1:cell_id[1]+2]=local_species.get_matrix()

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
        # TODO: Write this using is_instance instead, probably much nicer.
        return self.array[cell_id[0]][cell_id[1]].get_specie() is None 

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
        not_none_indices=[element for element in indices if element not in none_indices]

        # Randomize priority. Idea: choose priority rules based on how long they have gone without food and age.
        # Might not be good to observe chaos.
        np.random.shuffle(not_none_indices) 

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