import numpy as np
from grid import Grid
from cell import Cell, Empty_Cell, Shark, Fish, Crill, Algae
import numpy as np
from grid import Grid
from cell import Cell, Empty_Cell, Shark, Fish, Crill, Algae
import matplotlib.pyplot as plt
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore, QtWidgets
import random
import concurrent.futures
import csv


def create_random_grid_with_probabilities(size, values, probabilities, max_ages=[50, 50, 50], lay_egg=False, meals_for_birth=[1, 1, 1], separate_gender=False):
    """
    Create a 2D numpy.ndarray containing species
    values: list of classes 
    probabilities: list of probabilities for the initial values.
    The etries are the probabilities for each gridbox to be a certain specie
    max_ages: list of the ages at which the Shark, Fish and Crill die.
    lay_egg: boolean that determines whether all species lay egg or give birth
    meals_for_birth: If they give birth, this list determines how many meals each specie must have to give birth
    spearate_genders: boolean determining whether to separate women and men. 
    Only women give birth to either kids or eggs.
    """
    def create_instance(value):
        """Helper function to create instances of the objects, with arguments where necessary."""
        if value == Shark:
            return Shark(max_age=max_ages[0], lay_egg=lay_egg, meals_for_birth=meals_for_birth[0], separate_gender=separate_gender)
        if value == Fish:
            return Fish(max_age=max_ages[1], lay_egg=lay_egg, meals_for_birth=meals_for_birth[1], separate_gender=separate_gender)
        if value == Crill:
            return Crill(max_age=max_ages[2], lay_egg=lay_egg, meals_for_birth=meals_for_birth[2], separate_gender=separate_gender)     
        return value()  
        
    return np.array([
        [create_instance(random.choices(values, probabilities)[0]) for _ in range(size[0])]
        for _ in range(size[1])
    ])

def run_update(pre_grid, iter=10, plot_number_of_species=True, return_numbers=False):
    """
    Updates pre_grid, iter times and plots the number of all species if required.
    pre_grid: Grid with initial values
    iter: int with number of iterations to update
    plot_number_of_species: boolean
    return_numbers: boolean
    """
    for i in range(iter):
        pre_grid.update()
    if plot_number_of_species:
        plt.figure()
        algae_nbrs, crill_nbrs, fish_nbrs, shark_nbrs=pre_grid.get_numbers()
        plt.plot(algae_nbrs, 'g', label='Algae')
        plt.plot(crill_nbrs, 'b', label='Crill')
        plt.plot(fish_nbrs, 'r', label='Fish')
        plt.plot(shark_nbrs, 'k', label='Shark')
        plt.xlabel('iterations')
        plt.ylabel('number of species')
        plt.legend()
        plt.show()
    if (not plot_number_of_species) and return_numbers:
        algae_nbrs, crill_nbrs, fish_nbrs, shark_nbrs = pre_grid.get_numbers()
    if return_numbers:
        return algae_nbrs, crill_nbrs, fish_nbrs, shark_nbrs

def create_oscillation_with_three_grid(seed):
    """
    Returns a grid that yields oscillations with three species. The sharks die out
    """
    random.seed(seed)
    np.random.seed(seed)
    grid_size=(100,100)
    values = [Crill, Algae, Shark, Fish, Empty_Cell]
    probabilities = [0.2, 0.2, 0.01, 0.2, 0.29]
    max_ages=[10, 30, 100]
    lay_egg=False
    meals_for_birth=[1,2,1]
    separate_gender=True
    algae_probability=0.2
    meal_to_children=[0,0,0]
    grid = create_random_grid_with_probabilities(grid_size, values, probabilities, max_ages=max_ages, lay_egg=lay_egg, meals_for_birth=meals_for_birth, separate_gender=separate_gender)
    pre_grid=Grid(grid, allow_escape=True, algae_probability=algae_probability, meal_to_children=meal_to_children, max_ages=max_ages, lay_egg=lay_egg, meals_for_birth=meals_for_birth, separate_gender=separate_gender)
    return pre_grid

def create_oscillation_with_four_grid(probabilities, seed):
    """
    Returns a grid that yields oscillations with four species.
    probabilities: list of probabilities for the initial values.
    """
    random.seed(seed)
    np.random.seed(seed)
    grid_size=(100,100)
    values = [Crill, Algae, Shark, Fish, Empty_Cell]
    probabilities = probabilities
    max_ages=[5,100,100]
    lay_egg=True
    meals_for_birth=[0,0,0]
    separate_gender=False
    algae_probability=0.8
    meal_to_children=[1, 1/2, 4/3]
    grid = create_random_grid_with_probabilities(grid_size, values, probabilities, max_ages=max_ages, lay_egg=lay_egg, meals_for_birth=meals_for_birth, separate_gender=separate_gender)
    pre_grid=Grid(grid, allow_escape=True, algae_probability=algae_probability, meal_to_children=meal_to_children, max_ages=max_ages, lay_egg=lay_egg, meals_for_birth=meals_for_birth, separate_gender=separate_gender)
    return pre_grid

def get_numbers(i, iterations, probabilities):
    print(f'{i} started')
    pre_grid=create_oscillation_with_four_grid(probabilities, seed=i+1)
    algae_nbrs, crill_nbrs, fish_nbrs, shark_nbrs=run_update(pre_grid, iter=iterations, plot_number_of_species=False, return_numbers=True)
    print(f'{i} finished')
    return algae_nbrs, crill_nbrs, fish_nbrs, shark_nbrs

if __name__ == '__main__':  
    # # Option 1: Create grid that oscillates with three species
    # app=pg.mkQApp("WATOR")
    # pre_grid=create_oscillation_with_three_grid(seed=3)

    # # If we want to plot the grid. This requires grid to inherit from QWidgets.QWidget, 
    # # and for all code in grid.py that is commented out to be uncommented. Also the app above needs to be uncommented.
    # window=QtWidgets.QMainWindow()
    # window.resize(1200,600)
    # window.setCentralWidget(pre_grid)
    # window.show()
    # pg.exec()

    # If we just want to see the number of species as a function of time.
    # run_update(pre_grid, iter=100, plot_number_of_species=True)

    # Option 2: Reading and plotting data for four species. Parameters defined in create_oscillation_with_four_grid
    data_orig = np.genfromtxt('all_values_seed_50_iter_1000_init_20_20_40_20_0.csv', delimiter=',')
    data_change = np.genfromtxt('all_values_seed_50_iter_1000_init_20_19_41_20_0.csv', delimiter=',')
    # Split the data into separate arrays (columns)
    all_algae_nbrs1 = data_orig[:50, :]
    all_crill_nbrs1 = data_orig[50:100, :]
    all_fish_nbrs1 = data_orig[100:150, :]
    all_shark_nbrs1 = data_orig[150:, :]

    all_algae_nbrs2 = data_change[:50, :]
    all_crill_nbrs2 = data_change[50:100, :]
    all_fish_nbrs2 = data_change[100:150, :]
    all_shark_nbrs2 = data_change[150:, :]

    tot_algae_nbrs1=np.zeros((1000,2))
    tot_crill_nbrs1=np.zeros((1000,2))
    tot_fish_nbrs1=np.zeros((1000,2))
    tot_shark_nbrs1=np.zeros((1000,2))

    tot_algae_nbrs2=np.zeros((1000,2))
    tot_crill_nbrs2=np.zeros((1000,2))
    tot_fish_nbrs2=np.zeros((1000,2))
    tot_shark_nbrs2=np.zeros((1000,2))

    # Choosing simulations to plot. Only the ones for which no specie ddies out.
    for i in range(50):
        add_full_sim1=True
        add_full_sim2=True
        for j in range(1000):
            if not (all_algae_nbrs1[i,j]>0 and all_crill_nbrs1[i,j]>0 and all_fish_nbrs1[i,j]>0 and all_shark_nbrs1[i,j]>0):
                add_full_sim1=False
            if not (all_algae_nbrs2[i,j]>0 and all_crill_nbrs2[i,j]>0 and all_fish_nbrs2[i,j]>0 and all_shark_nbrs2[i,j]>0):
                add_full_sim2=False
        if add_full_sim1:
            tot_algae_nbrs1[:,0]+=all_algae_nbrs1[i,:]
            tot_algae_nbrs1[:,1]+=1
            tot_crill_nbrs1[:,0]+=all_crill_nbrs1[i,:]
            tot_crill_nbrs1[:,1]+=1
            tot_fish_nbrs1[:,0]+=all_fish_nbrs1[i,:]
            tot_fish_nbrs1[:,1]+=1
            tot_shark_nbrs1[:,0]+=all_shark_nbrs1[i,:]
            tot_shark_nbrs1[:,1]+=1
        if add_full_sim2:
            tot_algae_nbrs2[:,0]+=all_algae_nbrs2[i,:]
            tot_algae_nbrs2[:,1]+=1
            tot_crill_nbrs2[:,0]+=all_crill_nbrs2[i,:]
            tot_crill_nbrs2[:,1]+=1
            tot_fish_nbrs2[:,0]+=all_fish_nbrs2[i,:]
            tot_fish_nbrs2[:,1]+=1
            tot_shark_nbrs2[:,0]+=all_shark_nbrs2[i,:]
            tot_shark_nbrs2[:,1]+=1

    mean_algae_nbrs1=[tot_algae_nbr/nbr_of_non_zeros for tot_algae_nbr, nbr_of_non_zeros in zip(tot_algae_nbrs1[:,0], tot_algae_nbrs1[:,1])]
    mean_crill_nbrs1=[tot_crill_nbr/nbr_of_non_zeros for tot_crill_nbr, nbr_of_non_zeros in zip(tot_crill_nbrs1[:,0], tot_crill_nbrs1[:,1])]
    mean_fish_nbrs1=[tot_fish_nbr/nbr_of_non_zeros for tot_fish_nbr, nbr_of_non_zeros in zip(tot_fish_nbrs1[:,0], tot_fish_nbrs1[:,1])]
    mean_shark_nbrs1=[tot_shark_nbr/nbr_of_non_zeros for tot_shark_nbr, nbr_of_non_zeros in zip(tot_shark_nbrs1[:,0], tot_shark_nbrs1[:,1])]

    mean_algae_nbrs2=[tot_algae_nbr/nbr_of_non_zeros for tot_algae_nbr, nbr_of_non_zeros in zip(tot_algae_nbrs2[:,0], tot_algae_nbrs2[:,1])]
    mean_crill_nbrs2=[tot_crill_nbr/nbr_of_non_zeros for tot_crill_nbr, nbr_of_non_zeros in zip(tot_crill_nbrs2[:,0], tot_crill_nbrs2[:,1])]
    mean_fish_nbrs2=[tot_fish_nbr/nbr_of_non_zeros for tot_fish_nbr, nbr_of_non_zeros in zip(tot_fish_nbrs2[:,0], tot_fish_nbrs2[:,1])]
    mean_shark_nbrs2=[tot_shark_nbr/nbr_of_non_zeros for tot_shark_nbr, nbr_of_non_zeros in zip(tot_shark_nbrs2[:,0], tot_shark_nbrs2[:,1])]

    algae_diff=[np.abs(algae_1-algae_2) for algae_1, algae_2 in zip(mean_algae_nbrs1, mean_algae_nbrs2)]
    crill_diff=[np.abs(crill_1-crill_2) for crill_1, crill_2 in zip(mean_crill_nbrs1, mean_crill_nbrs2)]
    fish_diff=[np.abs(fish_1-fish_2) for fish_1, fish_2 in zip(mean_fish_nbrs1, mean_fish_nbrs2)]
    shark_diff=[np.abs(shark_1-shark_2) for shark_1, shark_2 in zip(mean_shark_nbrs1, mean_shark_nbrs2)]
    all_species_diff=[np.linalg.norm([algae_diff[i], crill_diff[i], fish_diff[i], shark_diff[i]], 2) for i in range(1000)]
    
    plt.figure()
    plt.plot(mean_crill_nbrs1[:200], 'b', label='Crill')
    plt.plot(mean_fish_nbrs1[:200], 'r', label='Fish')
    plt.plot(mean_shark_nbrs1[:200], 'k', label='Shark')
    plt.plot(mean_algae_nbrs1[:200], 'g', label='Algae')
    plt.xlabel('iterations')
    plt.ylabel('number of species (mean over different seeds)')
    plt.legend()

    plt.figure()
    plt.plot(mean_crill_nbrs2[:200], 'b', label='Crill')
    plt.plot(mean_fish_nbrs2[:200], 'r', label='Fish')
    plt.plot(mean_shark_nbrs2[:200], 'k', label='Shark')
    plt.plot(mean_algae_nbrs2[:200], 'g', label='Algae')
    plt.xlabel('iterations')
    plt.ylabel('number of species (mean over different seeds)')
    plt.legend()

    plt.figure()
    plt.plot(all_species_diff)
    plt.xlabel('iterations')
    plt.ylabel('deltax(iterations)')
    plt.show()

    # # Creating data for four species ALREADY SAVED IN FILES, DO NOT RUN.
    # all_algae_nbrs=[]
    # all_crill_nbrs=[]
    # all_fish_nbrs=[]
    # all_shark_nbrs=[]
    # nbr_of_seeds=50
    # iterations=1000
    # probabilities=[0.20, 0.20, 0.40, 0.20, 0]

    # # Creating the thread pool 
    # with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
    #     # Submitting tasks to the thread pool
    #     futures = [executor.submit(get_numbers, i, iterations, probabilities) for i in range(nbr_of_seeds)]
    #     for future in concurrent.futures.as_completed(futures):
    #         algae_nbrs, crill_nbrs, fish_nbrs, shark_nbrs=future.result()
    #         all_algae_nbrs.append(algae_nbrs)
    #         all_crill_nbrs.append(crill_nbrs)
    #         all_fish_nbrs.append(fish_nbrs)
    #         all_shark_nbrs.append(shark_nbrs)

    # with open('all_values_seed_50_iter_1000_init_20_20_40_20_0.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)

    #     for i in range(len(all_algae_nbrs)):
    #         writer.writerow(all_algae_nbrs[i])
    #     for i in range(len(all_crill_nbrs)):
    #         writer.writerow(all_crill_nbrs[i])
    #     for i in range(len(all_fish_nbrs)):
    #         writer.writerow(all_fish_nbrs[i])
    #     for i in range(len(all_shark_nbrs)):
    #         writer.writerow(all_shark_nbrs[i])