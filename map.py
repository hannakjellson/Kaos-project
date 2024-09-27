import numpy as np
COLORS=['b','g','r','c','m','y','k','w']
GRID_SIZE=(10,10)
SPECIES=[1,2]
INIT_VALUES=np.ones(GRID_SIZE)# Should be an array of cells. Potentially read from interactive window later.

class Grid():
    def __init__(self, size, array):
        self.size=size
        self.array=array

    def __getitem__(self, indices):
        i,j=indices
        return self.array[i][j]

    def get_matrix(self):
        # Return the grid as a numpy array
        return self.array
    
    def get_center(self):
        # TODO return center of the map
        pass

    def get_local_species(self, cell_id):
        # TODO: make it work at borders. Return grid of values around cell_id maybe return as a grid, so we can implement a get_center method here.
        pass
    
    def set_local_species(self, cell_id, local_species):
        # TODO: update neighbouring values around cell_id
        pass

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
        moved_species_grid=Grid(GRID_SIZE, np.empty(GRID_SIZE))
        for index in indices:
            if self.array[index].specie() in SPECIES:
                local_species=self.get_local_species(index)
                moved_local_species=moved_species_grid.get_local_species(index)
                self.array[index], updated_moved_local_species=self.array[index].update(local_species, moved_local_species)
                moved_species_grid.set_local_species(index, updated_moved_local_species)
            

class Cell():
    def __init__(self, specie):
        self.specie=specie
    
    def update(self, local_species, moved_local_species):
        """ Updates the value in the gridbox grid_box.
        grid_box: the gridbox
        neighbours: values in surrounding gridboxes
        maps: dict with the possible gridboxes with surrounding.
        colors: """
        updated_center=moved_local_species.get_center().specie() 
        if updated_center is not None:
            return Cell(updated_center), moved_local_species # I guess we can ignore what in the cell before after this.
        return self.update(local_species, moved_local_species)

class Empty_Cell(Cell):

    def __init__(self):    
        super().__init__()

    def specie(self):
        return None
  
    def update(self, local_species, moved_local_species):
        # TODO: implement something for the update in the end i guess.
        pass

class Fish(Cell):

    def __init__(self, has_moved):
        super().__init__()
        self.has_moved=has_moved

    def specie(self):
        if self.has_moved:
            return -1
        return 1
    
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
        super().__init__()
        self.has_moved=has_moved

    def specie(self):
        if self.has_moved:
            return -2
        return 2

    def update(self, local_species, moved_local_species):
        # 1 and moved to is not 2 or 1=> ok to go to
        # -1 and moved to is not 2 => ok to go to
        fish_indices=np.argwhere((local_species.to_matrix()==1 and moved_local_species.to_matrix() is None) or moved_local_species.to_matrix()==-1)
        if fish_indices is not None:
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
        pre_grid=Grid(GRID_SIZE, INIT_VALUES)
        pre_grid.update()


        
        
    
    # def get_none_indices(self):
    #     none_indices = []
    #     for i, row in enumerate(self.array):
    #         for j, element in enumerate(row):
    #             if element.specie() is None:
    #                 none_indices.append((i, j)) # Don't think that the element itself will be None.
    #     return none_indices

    # def random_none_index(self):
    #     none_indices = self.get_none_indices()  # Get list of all None indices
    #     if none_indices:
    #         return np.random.choice(none_indices)  # Randomly select one index
    #     else:
    #         return None