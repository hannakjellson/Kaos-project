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
        I am not using this anymore.
        """
        become_algae=random.random()<=probability

        return Algae() if become_algae else self
        

class Shark(Cell):

    def __init__(self, age=None, meals=None, had_meal=None, max_age=50, lay_egg=False, meals_for_birth=1, separate_gender=False):
        """
        Initialize Shark cell
        age: int, age of shark
        meals: int, number of meals eaten
        had_meal: boolean, if the shark had a meal in the last round
        max_age: int, the age the shark dies
        lay_egg: boolean, if the shark lays egg
        meals_for_birth: int, how many meals the shark should eat to give birth
        separate_gender: boolean, if there are both male and female sharks.
        """
        self.max_age=max_age
        self.lay_egg=lay_egg
        self.age=random.randint(0,self.max_age) if age is None else age
        self.meals=random.randint(0,1) if meals is None else meals
        self.had_meal=np.random.choice([True, False]) if had_meal is None else had_meal
        self.meals_for_birth=meals_for_birth
        self.separate_gender=separate_gender
        if separate_gender:
            self.is_woman = np.random.choice([True, False])
        else:
            self.is_woman=True
        super().__init__((50, 50, 50)) if self.is_woman else super().__init__((0, 0, 0))

    def update(self, local_species, moved_local_species):
        """
        Update Shark Cell based on surroundings
        local_species: Grid of this Shark and its surrounding Cells
        moved_local_species: Grid describing how surrounding Cells have already moved in this iteration
        """
        if self.age==self.max_age:
            # Shark dies
            moved_local_species.set_specie((1,1),Empty_Cell())
        else:
            # Saving the number of meals and if it had a meal in the previous round for later
            pre_meals=self.meals
            pre_had_meal=self.had_meal

            # Find fish indices that have not already been eaten
            present_fish_indices=local_species.where_fish()
            still_empty_indices=moved_local_species.where_none()
            stuck_fish_indices=moved_local_species.where_fish()
            fish_indices=np.argwhere(np.logical_and(present_fish_indices, np.logical_or(still_empty_indices, stuck_fish_indices)))
            fish_indices=[tuple(fish_index) for fish_index in fish_indices]
            self.had_meal=False

            # Try to eat
            if len(fish_indices)>0:
                move_to=random.choice(fish_indices)
                moved_local_species.set_specie(move_to, self)
                if self.priority<local_species[move_to].get_priority() or move_to in np.argwhere(np.logical_and(present_fish_indices, stuck_fish_indices)):
                    self.had_meal=True
                    self.meals+=1
            else:
                move_to=local_species.get_random_common_none_index(moved_local_species)
            
            # If we have somewhere to move
            if move_to is not None:
                # If possible, give birth to a new shark. If we are stuck, we simply do not give birth.
                if (not self.lay_egg) and self.is_woman and pre_had_meal==True and pre_meals!=0 and pre_meals % self.meals_for_birth == 0:
                    moved_local_species.set_specie((1,1), Shark(0,0,False, max_age=self.max_age, lay_egg=self.lay_egg, meals_for_birth=self.meals_for_birth, separate_gender=self.separate_gender))
                moved_local_species.set_specie(move_to,self)
            # If we are stuck. 
            else: 
                moved_local_species.set_specie((1,1), self)
        self.age+=1
        return moved_local_species
    
class Fish(Cell):
    def __init__(self, age=None, meals=None, had_meal=None, max_age=50, lay_egg=False, meals_for_birth=1, separate_gender=False):
        """
        Initialize Fish cell
        age: int, age of fish
        meals: int, number of meals eaten
        had_meal: boolean, if the fish had a meal in the last round
        max_age: int, the age the fish dies
        lay_egg: boolean, if the fish lays egg
        meals_for_birth: int, how many meals the fish should eat to give birth
        separate_gender: boolean, if there are both male and female fish.
        """
        self.max_age=max_age
        self.lay_egg=lay_egg
        self.age=random.randint(0,self.max_age) if age is None else age
        self.meals=random.randint(0,2) if meals is None else meals
        self.had_meal=np.random.choice([True, False]) if had_meal is None else had_meal
        self.meals_for_birth=meals_for_birth
        self.separate_gender=separate_gender
        if separate_gender:
            self.is_woman = np.random.choice([True, False])
        else:
            self.is_woman=True
        super().__init__((255, 0, 0)) if self.is_woman else super().__init__((200, 0, 0))
    
    def update(self, local_species, moved_local_species):
        """
        Update Fish Cell based on surroundings
        local_species: Grid of this Fish and its surrounding Cells
        moved_local_species: Grid describing how surrounding Cells have already moved in this iteration
        """
        # If we have not been eaten by a shark already
        if isinstance(moved_local_species[(1,1)], Empty_Cell) and not self.age==self.max_age:
            # Saving the number of meals and if it had a meal in the previous round for later
            pre_meals=self.meals
            pre_had_meal=self.had_meal

            # Find crill indices that have not already been eaten
            present_crill_indices=local_species.where_crill()
            still_empty_indices=moved_local_species.where_none()
            stuck_crill_indices=moved_local_species.where_crill()
            crill_indices=np.argwhere(np.logical_and(present_crill_indices, np.logical_or(still_empty_indices, stuck_crill_indices)))
            crill_indices=[tuple(crill_index) for crill_index in crill_indices]
            self.had_meal=False

            # Try to eat
            if len(crill_indices)>0:
                move_to=random.choice(crill_indices)
                if self.priority<local_species[move_to].get_priority() or move_to in np.argwhere(np.logical_and(present_crill_indices, stuck_crill_indices)):
                    self.had_meal=True
                    self.meals+=1
            else:
                move_to=local_species.get_random_common_none_index(moved_local_species)

            # If we have somewhere to move
            if move_to is not None:
                if (not self.lay_egg) and self.is_woman and pre_had_meal and pre_meals!=0 and pre_meals % self.meals_for_birth == 0:
                    moved_local_species.set_specie((1,1), Fish(0, 0, False, max_age=self.max_age, lay_egg=self.lay_egg, meals_for_birth=self.meals_for_birth, separate_gender=self.separate_gender))
                moved_local_species.set_specie(move_to, self)         
            # If we are stuck
            else: 
                moved_local_species.set_specie((1,1), self)
        self.age+=1
        return moved_local_species

class Crill(Cell):
    def __init__(self, age=None, meals=None, had_meal=None, max_age=50, lay_egg=False, meals_for_birth=1, separate_gender=False):
        """
        Initialize Crill cell
        age: int, age of crill
        meals: int, number of meals eaten
        had_meal: boolean, if the crill had a meal in the last round
        max_age: int, the age the crill dies
        lay_egg: boolean, if the crill lays egg
        meals_for_birth: int, how many meals the shark should eat to give birth
        separate_gender: boolean, if there are both male and female crill.
        """
        self.max_age=max_age
        self.lay_egg=lay_egg
        self.age=random.randint(0,self.max_age) if age is None else age
        self.meals=random.randint(0,1) if meals is None else meals
        self.had_meal=np.random.choice([True, False]) if had_meal is None else had_meal
        self.meals_for_birth=meals_for_birth
        self.separate_gender=separate_gender
        if separate_gender:
            self.is_woman = np.random.choice([True, False])
        else:
            self.is_woman=True
        super().__init__((100, 100, 255)) if self.is_woman else super().__init__((50, 50, 220))

    def update(self, local_species, moved_local_species):
        """
        Update Crill Cell based on surroundings
        local_species: Grid of this Crill and its surrounding Cells
        moved_local_species: Grid describing how surrounding Cells have already moved in this iteration
        """
        # If we have not been eaten by a fish already
        if isinstance(moved_local_species[(1,1)], Empty_Cell) and not self.age==self.max_age:
            # Saving the number of meals and if it had a meal in the previous round for later
            pre_meals=self.meals
            pre_had_meal=self.had_meal

            # Find algae indices that were not already eaten
            is_algae_matrix=moved_local_species.where_algae()
            algae_indices=np.argwhere(is_algae_matrix)
            algae_indices=[tuple(algae_index) for algae_index in algae_indices]

            # Try to eat
            if len(algae_indices)>0:
                move_to=random.choice(algae_indices)
                self.had_meal=True
                self.meals+=1
            else:
                self.had_meal=False
                move_to=local_species.get_random_common_none_index(moved_local_species)

            # If we have somewhere to move
            if move_to is not None:
                if (not self.lay_egg) and self.is_woman and pre_had_meal and pre_meals % self.meals_for_birth == 0:
                    moved_local_species.set_specie((1,1), Crill(0,0,False, max_age=self.max_age, lay_egg=self.lay_egg, meals_for_birth=self.meals_for_birth, separate_gender=self.separate_gender))
                moved_local_species.set_specie(move_to, self)
                 
            # If we are stuck
            else: 
                moved_local_species.set_specie((1,1), self)
        self.age+=1    
        return moved_local_species

class Algae(Cell):
    def __init__(self):
        """
        Initialize Algae cell
        """
        super().__init__((0, 255, 0))

    def update(self, local_species, moved_local_species):
        moved_local_species.set_specie((1,1), Algae())
        return moved_local_species
