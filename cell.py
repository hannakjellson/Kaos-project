import numpy as np
import random

class Cell():
    def __init__(self, color):
        """
        Initialize Cell
        specie: int or None
        """
        self.color=color
        self.priority=None
    
    def getColor(self):
        return self.color
    
    def set_priority(self, priority):
        self.priority=priority

    def get_priority(self):
        return self.priority
    
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
        super().__init__((255,255,255))
  
    def update(self, probability):
        """"
        Should not happen, an Empty Cell is only updated based on how the species move.
        """
        become_algae=random.random()<=probability

        return Algae() if become_algae else self
        

class Shark(Cell):

    def __init__(self, age=None, meals=None, had_meal=None):
        """
        Initialize Shark cell
        """
        self.max_age=50
        self.age=random.randint(0,self.max_age) if age is None else age
        self.meals=random.randint(0,2) if meals is None else meals
        self.had_meal=np.random.choice([True, False]) if had_meal is None else had_meal
        self.is_woman=np.random.choice([True, False])
        super().__init__((50, 50, 50)) if self.is_woman else super().__init__((0, 0, 0))
        self.meals_for_birth=2

    def update(self, local_species, moved_local_species):
        """
        Update Shark Cell based on surroundings
        local_species: Grid of this Shark and its surrounding Cells
        moved_local_species: Grid describing how surrounding Cells have already moved in this iteration
        """
        if self.age==self.max_age:
            # Shark dies
            moved_local_species.set_specie(moved_local_species.get_center(),Empty_Cell())
        else:
            # Saving the number of meals and if it had a meal in the previous round for later
            pre_meals=self.meals
            pre_had_meal=self.had_meal

            # Find fish indices that have not already been eaten
            is_fish = np.vectorize(lambda cell: isinstance(cell, Fish))
            is_empty = np.vectorize(lambda cell: isinstance(cell, Empty_Cell))
            present_fish_indices=is_fish(local_species.get_matrix())
            still_empty_indices=is_empty(moved_local_species.get_matrix())
            stuck_fish_indices=is_fish(moved_local_species.get_matrix())
            fish_indices=np.argwhere(np.logical_and(present_fish_indices, np.logical_or(still_empty_indices, stuck_fish_indices)))
            fish_indices=[tuple(fish_index) for fish_index in fish_indices]

            if len(fish_indices)>0:
                # Problem here: it does not eat everytime we get here.
                move_to=random.choice(fish_indices)
                moved_local_species.set_specie(move_to, self)
                if self.priority<local_species[move_to].get_priority() or move_to in np.argwhere(stuck_fish_indices):
                    self.had_meal=True
                    self.meals+=1
            else:
                self.had_meal=False
                move_to=local_species.get_random_common_none_index(moved_local_species)
                # If we have somewhere to move
            
            if move_to is not None:
                # If possible, give birth to a new shark. If we are stuck, we simply do not give birth.
                if self.is_woman and pre_had_meal==True and pre_meals % self.meals_for_birth == 0:
                    moved_local_species.set_specie(moved_local_species.get_center(), Shark(0,0,False))
                moved_local_species.set_specie(move_to,self)
            # If we are stuck. 
            else: 
                moved_local_species.set_specie(moved_local_species.get_center(), self)
        self.age+=1
        return moved_local_species
    
class Fish(Cell):
    def __init__(self, age=None, meals=None, had_meal=None):
        """
        Initialize Fish cell
        has_moved: boolean. False if there is a Fish in the Cell, True if the Fish left in this iteration
        """
        self.max_age=100
        self.age=random.randint(0,self.max_age) if age is None else age
        self.meals=random.randint(0,2) if meals is None else meals
        self.had_meal=np.random.choice([True, False]) if had_meal is None else had_meal
        self.is_woman=np.random.choice([True, False])
        super().__init__((255, 0, 0)) if self.is_woman else super().__init__((200, 0, 0))
        self.meals_for_birth=2
    
    def update(self, local_species, moved_local_species):
        """
        Update Fish Cell based on surroundings
        local_species: Grid of this Fish and its surrounding Cells
        moved_local_species: Grid describing how surrounding Cells have already moved in this iteration
        """
        # If we have not been eaten by a shark already
        if isinstance(moved_local_species[moved_local_species.get_center()], Empty_Cell) and not self.age==self.max_age:
            # Saving the number of meals and if it had a meal in the previous round for later
            pre_meals=self.meals
            pre_had_meal=self.had_meal

            # Find crill indices that have not already been eaten
            is_crill = np.vectorize(lambda cell: isinstance(cell, Crill))
            is_empty = np.vectorize(lambda cell: isinstance(cell, Empty_Cell))
            present_crill_indices=is_crill(local_species.get_matrix())
            still_empty_indices=is_empty(moved_local_species.get_matrix())
            stuck_crill_indices=is_crill(moved_local_species.get_matrix())
            crill_indices=np.argwhere(np.logical_and(present_crill_indices, np.logical_or(still_empty_indices, stuck_crill_indices)))
            crill_indices=[tuple(crill_index) for crill_index in crill_indices]
            if len(crill_indices)>0:
                move_to=random.choice(crill_indices)
                if self.priority<local_species[move_to].get_priority() or move_to in np.argwhere(stuck_crill_indices):
                    self.had_meal=True
                    self.meals+=1
            else:
                self.had_meal=False
                move_to=local_species.get_random_common_none_index(moved_local_species)

            # If we have somewhere to move
            if move_to is not None:
                if self.is_woman and pre_had_meal and pre_meals % self.meals_for_birth == 0:
                    moved_local_species.set_specie(moved_local_species.get_center(), Fish(0,0,False))
                moved_local_species.set_specie(move_to, self)         
            # If we are stuck
            else: 
                moved_local_species.set_specie(moved_local_species.get_center(), self)
        self.age+=1
        return moved_local_species

class Crill(Cell):
    def __init__(self, age=None, meals=None, had_meal=None):
        self.max_age=50
        self.age=random.randint(0,self.max_age) if age is None else age
        self.meals=random.randint(0,2) if meals is None else meals# Improve initialization.
        self.had_meal=np.random.choice([True, False]) if had_meal is None else had_meal
        self.is_woman=np.random.choice([True, False])
        super().__init__((100, 100, 255)) if self.is_woman else super().__init__((50, 50, 220))
        self.meals_for_birth=2

    def update(self, local_species, moved_local_species):
        """
        Update Crill Cell based on surroundings
        local_species: Grid of this Crill and its surrounding Cells
        moved_local_species: Grid describing how surrounding Cells have already moved in this iteration
        """
        # If we have been eaten by a fish already
        if isinstance(moved_local_species[moved_local_species.get_center()], Empty_Cell) and not self.age==self.max_age:
            # Saving the number of meals and if it had a meal in the previous round for later
            pre_meals=self.meals
            pre_had_meal=self.had_meal

            # Find algae indices that were not already eaten
            is_algae = np.vectorize(lambda cell: isinstance(cell, Algae))
            is_algae_matrix=is_algae(moved_local_species.get_matrix())
            algae_indices=np.argwhere(is_algae_matrix)
            algae_indices=[tuple(algae_index) for algae_index in algae_indices]
            if len(algae_indices)>0:
                move_to=random.choice(algae_indices)
                self.had_meal=True
                self.meals+=1
            else:
                self.had_meal=False
                move_to=local_species.get_random_common_none_index(moved_local_species)

            # If we have somewhere to move
            if move_to is not None:
                if self.is_woman and pre_had_meal and pre_meals % self.meals_for_birth == 0:
                    moved_local_species.set_specie(moved_local_species.get_center(), Crill(0,0,False))
                moved_local_species.set_specie(move_to, self)
            # If we are stuck
            else: 
                moved_local_species.set_specie(moved_local_species.get_center(), self)
        self.age+=1    
        return moved_local_species

class Algae(Cell):
    def __init__(self):
        """
        Initialize Algae cell
        """
        super().__init__((0, 255, 0))

    def update(self, local_species, moved_local_species):
        moved_local_species.set_specie(moved_local_species.get_center(), Algae())
        return moved_local_species
        