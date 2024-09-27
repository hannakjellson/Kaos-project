import numpy as np
COLORS=['b','g','r','c','m','y','k','w']
GRID_SIZE=(10,10)
SPECIES=[1,2]

class Grid():
    def __init__(self, array):
        self.size=np.shape(array)
        self.array=array

    def __getitem__(self, indices):
        i,j=indices
        return self.array[i][j]

    def get_matrix(self):
        # Return the grid as a numpy array
        return self.array
    
    def get_center(self):
        # TODO generalize for other shapes of the cells
        return (1,1)

    def get_local_species(self, cell_id):
        # TODO: make it work at borders. Return grid of values around cell_id maybe return as a grid, so we can implement a get_center method here.
        return Grid(self.array[cell_id[0]-1:cell_id[0]+1,cell_id[1]-1:cell_id[1]+1])
    
    def set_local_species(self, cell_id, local_species):
        self.array[cell_id[0]-1:cell_id[0]+1,cell_id[1]-1:cell_id[1]+1]=local_species # Can I do this?

    def is_none(self, i, j):
        return self.array[i][j] is None 
    
    def random_common_none_index(self, other_grid):
        common_none_indices = []

        # Loop through all indices to find where both matrices have None
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.is_none(i, j) and other_grid.is_none(i, j) and i != self.get_center()[0] and j!= self.get_center()[1]:
                    common_none_indices.append((i, j))

        # Randomly pick an index from the common None indices, I guess it makes sense to not allow it to go where a previous specie was before, 
        # as it wouldnt know that the other specie has moved
        if common_none_indices:
            return np.random.choice(common_none_indices)
        else:
            return None  # Return None if no common None indices are found
    
    def update(self):
        indices = np.array([(i, j) for i in range(GRID_SIZE[0]) for j in range(GRID_SIZE[1])])
        np.random.shuffle(indices) # Idea: choose priority rules based on how long they have gone without food and age.
        empty_array=np.empty(GRID_SIZE, dtype=object)
        empty_array[empty_array==None]=Empty_Cell() # Should be possible to write better.
        moved_species_grid=Grid(empty_array)
        for index in indices:
            i,j=index
            if self.array[i][j].get_specie() in SPECIES:
                local_species=self.get_local_species(index)
                moved_local_species=moved_species_grid.get_local_species(index)
                self.array[i][j], updated_moved_local_species=self.array[i][j].update(local_species, moved_local_species)
                moved_species_grid.set_local_species(index, updated_moved_local_species)
        return self.array
            

class Cell():
    def __init__(self, specie):
        self.specie=specie

    def get_specie(self):
        return self.specie
    
    def update(self, local_species, moved_local_species):
        """ Updates the value in the gridbox grid_box.
        grid_box: the gridbox
        neighbours: values in surrounding gridboxes
        maps: dict with the possible gridboxes with surrounding.
        colors: """
        raise NotImplementedError("Should be implemented in the subclass")
        # updated_center=moved_local_species.get_center().get_specie() 
        # # Loop through all non-empty cells.
        # if updated_center is not None:
        #     return Cell(updated_center), moved_local_species # I guess we can ignore what was in the cell before, after this.
        # return self.update(local_species, moved_local_species)

class Empty_Cell(Cell):

    def __init__(self):    
        super().__init__(None)
  
    def update(self, local_species, moved_local_species):
        # Should not happen.
        pass

class Fish(Cell):

    def __init__(self, has_moved):
        if has_moved:
            super().__init__(-1)
        else:
            super().__init__(1)
        self.has_moved=has_moved
    
    def update(self, local_species, moved_local_species):
        if moved_local_species.get_center() is not None:
            # moved_local_species.get_center()=Fish(True) # Maybe not necessary as it died.
            return Shark(False), moved_local_species
        move_to=local_species.random_common_none_index(moved_local_species)
        if move_to is not None:
            # If we have somewhere to move
            moved_local_species[move_to]=Fish(False)
            moved_local_species[moved_local_species.get_center()]=Fish(True)
            return Empty_Cell(None), moved_local_species
        else: 
            # If we are stuck
            return self, moved_local_species

class Shark(Cell):

    def __init__(self, has_moved):
        if has_moved:
            super().__init__(-2)
        else:
            super().__init__(2)
        self.has_moved=has_moved

    def update(self, local_species, moved_local_species):
        # 1 and moved to is not 2 or 1=> ok to go to
        # -1 and moved to is not 2 => ok to go to
        fish_indices=np.argwhere(np.logical_or(np.logical_and(local_species.get_matrix()==1, moved_local_species.get_matrix() == None), moved_local_species.get_matrix()==-1))
        if fish_indices.size>0:
            move_to=np.random.choice(fish_indices)
            moved_local_species[move_to]=Shark(False)
            moved_local_species[moved_local_species.get_center()]=Shark(True)
            return Empty_Cell(), moved_local_species
        else:
            move_to=local_species.random_common_none_index(moved_local_species)
            if move_to is not None:
                # If we have somewhere to move
                moved_local_species[move_to]=Shark(False)
                moved_local_species[moved_local_species.get_center()]=Shark(True)
                return Empty_Cell(None), moved_local_species
            else: 
                # If we are stuck
                return self, moved_local_species


if __name__ == '__main__':  
    init_values=np.empty(GRID_SIZE, dtype=object)# Should be an array of cells. Potentially read from interactive window later.
    init_values[5,5]=Shark(False)
    init_values[1,3]=Fish(False)
    init_values[init_values == None]=Empty_Cell()
    pre_grid=Grid(init_values)
    print(pre_grid.update() is not Empty_Cell)



        
        
    
    # def get_none_indices(self):
    #     none_indices = []
    #     for i, row in enumerate(self.array):
    #         for j, element in enumerate(row):
    #             if element.get_specie() is None:
    #                 none_indices.append((i, j)) # Don't think that the element itself will be None.
    #     return none_indices

    # def random_none_index(self):
    #     none_indices = self.get_none_indices()  # Get list of all None indices
    #     if none_indices:
    #         return np.random.choice(none_indices)  # Randomly select one index
    #     else:
    #         return None