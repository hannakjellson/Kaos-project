import numpy as np

class Cell():
    def __init__(self, specie):
        """
        Initialize Cell
        specie: int or None
        """
        self.specie=specie

    def get_specie(self):
        """
        Returns specie
        """
        return self.specie
    
    def update(self):
        """
        Updates the specie in the Cell
        """
        raise NotImplementedError("Should be implemented in the subclass")

class Empty_Cell(Cell):
    def __init__(self):
        """
        Initialize Empty_Cell
        """    
        super().__init__(None)
  
    def update(self):
        """"
        Should not happen, an Empty Cell is only updated based on how the species move.
        """
        raise NotImplementedError("An Empty_Cell cannot be updated on its own")

class Fish(Cell):
    def __init__(self, has_moved=False):
        """
        Initialize Fish cell
        has_moved: boolean. False if there is a Fish in the Cell, True if the Fish left in this iteration
        """
        if has_moved:
            super().__init__(-1)
        else:
            super().__init__(1)
        self.has_moved=has_moved
    
    def update(self, local_species, moved_local_species):
        """
        Update Fish Cell based on surroundings
        local_species: Grid of this Fish and its surrounding Cells
        moved_local_species: Grid describing how surrounding Cells have already moved in this iteration
        """
        # If we have been eaten by a shark already
        if moved_local_species[moved_local_species.get_center()].get_specie() != None:
            return Shark(), moved_local_species
        
        move_to=local_species.get_random_common_none_index(moved_local_species)

        # If we have somewhere to move
        if move_to is not None:
            moved_local_species.set_specie(move_to,Fish())
            moved_local_species.set_specie(moved_local_species.get_center(),Fish(True))
            return Empty_Cell(), moved_local_species
        
        # If we are stuck
        else: 
            # We need to go through all these cells again, to see whether they changed
            moved_local_species[moved_local_species.get_center()]=Cell(0)
            return self, moved_local_species

class Shark(Cell):

    def __init__(self, has_moved=False):
        """
        Initialize Shark cell
        has_moved: boolean. False if there is a Shark in the Cell, True if the Shark left in this iteration
        """
        if has_moved:
            super().__init__(-2)
        else:
            super().__init__(2)
        self.has_moved=has_moved

    def update(self, local_species, moved_local_species):
        """
        Update Shark Cell based on surroundings
        local_species: Grid of this Shark and its surrounding Cells
        moved_local_species: Grid describing how surrounding Cells have already moved in this iteration
        """
        # 1 and moved to is not 2 or 1=> ok to go to
        # -1 and moved to is not 2 => ok to go to
        fish_indices=np.argwhere(np.logical_or(np.logical_and(local_species.get_matrix()==1, moved_local_species.get_matrix() == None), moved_local_species.get_matrix()==-1))
        if fish_indices.size>0:
            move_to=np.random.choice(fish_indices)
            moved_local_species.set_specie(move_to, Shark())
            moved_local_species.set_specie(moved_local_species.get_center(), Shark(True))
            return Empty_Cell(), moved_local_species
        else:
            move_to=local_species.get_random_common_none_index(moved_local_species)
            print(move_to)
            if move_to is not None:
                # If we have somewhere to move
                moved_local_species.set_specie(move_to,Shark())
                moved_local_species.set_specie(moved_local_species.get_center(), Shark(True))
                return Empty_Cell(), moved_local_species
            else: 
                # If we are stuck
                return self, moved_local_species