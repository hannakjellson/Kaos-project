import numpy as np
import random

class Cell():
    def __init__(self, specie, color):
        """
        Initialize Cell
        specie: int or None
        """
        self.specie=specie
        self.color=color

    def get_specie(self):
        """
        Returns specie
        """
        return self.specie
    
    def getColor(self):
        return self.color
    
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
        super().__init__(None, (255,255,255))
  
    def update(self):
        """"
        Should not happen, an Empty Cell is only updated based on how the species move.
        """
        raise NotImplementedError("An Empty_Cell cannot be updated on its own")

class Fish(Cell):
    def __init__(self):
        """
        Initialize Fish cell
        has_moved: boolean. False if there is a Fish in the Cell, True if the Fish left in this iteration
        """
        super().__init__(1, (255, 100, 100))

    
    def update(self, local_species, moved_local_species):
        """
        Update Fish Cell based on surroundings
        local_species: Grid of this Fish and its surrounding Cells
        moved_local_species: Grid describing how surrounding Cells have already moved in this iteration
        """
        # If we have been eaten by a shark already
        if moved_local_species[moved_local_species.get_center()].get_specie() != None:
            return moved_local_species
        
        is_crill = np.vectorize(lambda cell: isinstance(cell, Crill))
        is_empty = np.vectorize(lambda cell: isinstance(cell, Empty_Cell))
        present_crill_indices=is_crill(local_species.get_matrix())
        still_empty_indices=is_empty(moved_local_species.get_matrix())
        stuck_crill_indices=is_crill(moved_local_species.get_matrix())
        crill_indices=np.argwhere(np.logical_and(present_crill_indices, np.logical_or(still_empty_indices, stuck_crill_indices)))
        crill_indices=[tuple(crill_index) for crill_index in crill_indices]
        if len(crill_indices)>0:
            move_to=random.choice(crill_indices)
            moved_local_species.set_specie(move_to, Fish())
            return moved_local_species
        
        move_to=local_species.get_random_common_none_index(moved_local_species)

        # If we have somewhere to move
        if move_to is not None:
            moved_local_species.set_specie(move_to,Fish())
            return moved_local_species
        
        # If we are stuck
        else: 
            return moved_local_species

class Shark(Cell):

    def __init__(self):
        """
        Initialize Shark cell
        """
        super().__init__(2, (0, 0, 0))

    def update(self, local_species, moved_local_species):
        """
        Update Shark Cell based on surroundings
        local_species: Grid of this Shark and its surrounding Cells
        moved_local_species: Grid describing how surrounding Cells have already moved in this iteration
        """
        # Find fish indices that have not already been eaten
        is_fish = np.vectorize(lambda cell: isinstance(cell, Fish))
        is_empty = np.vectorize(lambda cell: isinstance(cell, Empty_Cell))
        present_fish_indices=is_fish(local_species.get_matrix())
        still_empty_indices=is_empty(moved_local_species.get_matrix())
        stuck_fish_indices=is_fish(moved_local_species.get_matrix())
        fish_indices=np.argwhere(np.logical_and(present_fish_indices, np.logical_or(still_empty_indices, stuck_fish_indices)))
        fish_indices=[tuple(fish_index) for fish_index in fish_indices]
        if len(fish_indices)>0:
            move_to=random.choice(fish_indices)
            moved_local_species.set_specie(move_to, Shark())
            return moved_local_species
        else:
            move_to=local_species.get_random_common_none_index(moved_local_species)
            # If we have somewhere to move
            if move_to is not None:
                moved_local_species.set_specie(move_to,Shark())
                return moved_local_species
            # If we are stuck
            else: 
                moved_local_species.set_specie(moved_local_species.get_center(), Shark())
                return moved_local_species

class Crill(Cell):
    def __init__(self):
        super().__init__(3, (125, 125, 125))

    def update(self, local_species, moved_local_species):
        """
        Update Fish Cell based on surroundings
        local_species: Grid of this Fish and its surrounding Cells
        moved_local_species: Grid describing how surrounding Cells have already moved in this iteration
        """
        # If we have been eaten by a fish already
        if moved_local_species[moved_local_species.get_center()].get_specie() != None:
            return moved_local_species
        
        is_algae = np.vectorize(lambda cell: isinstance(cell, Algae))
        is_algae_matrix=is_algae(moved_local_species.get_matrix())
        algae_indices=np.argwhere(is_algae_matrix)
        algae_indices=[tuple(algae_index) for algae_index in algae_indices]
        if len(algae_indices)>0:
            move_to=random.choice(algae_indices)
            moved_local_species.set_specie(move_to, Crill())
            return moved_local_species
        
        move_to=local_species.get_random_common_none_index(moved_local_species)

        # If we have somewhere to move
        if move_to is not None:
            moved_local_species.set_specie(move_to,Crill())
            return moved_local_species
        
        # If we are stuck
        else: 
            return moved_local_species

class Algae(Cell):
    def __init__(self):
        """
        Initialize Algae cell
        """
        super().__init__(4, (0, 255, 0))

    def update(self, local_species, moved_local_species):
        moved_local_species.set_specie(moved_local_species.get_center(), Algae())
        return moved_local_species
        