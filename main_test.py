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
    # app=pg.mkQApp("WATOR")
    # # Create grid that oscillates with three species
    # pre_grid=create_oscillation_with_three_grid(seed=3)

    # Create grid that oscillates with four species
    probabilities=[0.20, 0.19, 0.41, 0.20, 0]
    pre_grid=create_oscillation_with_four_grid(probabilities, seed=2)

    # If we want to plot the grid. This requires grid to inherit from QWidgets.QWidget, 
    # and for all code in grid.py that is commented out to be uncommented.
    # window=QtWidgets.QMainWindow()
    # window.resize(1200,600)
    # window.setCentralWidget(pre_grid)
    # window.show()
    # pg.exec()

    # # If we just want to see the number of species as a function of time.
    run_update(pre_grid, iter=1000, plot_number_of_species=True)

    # # Create two grids to calculate Lyapunov Exponents
    # probabilities_1=[0.20, 0.20, 0.20, 0.20, 0.20]
    # pre_grid_1=create_oscillation_with_four_grid(probabilities_1, seed=1)
    # algae_nbrs_1, crill_nbrs_1, fish_nbrs_1, shark_nbrs_1=run_update(pre_grid_1, iter=100, plot_number_of_species=False, return_numbers=True)
    
    # probabilities_2=[0.20, 0.20, 0.20, 0.20, 0.20]
    # pre_grid_2=create_oscillation_with_four_grid(probabilities_2, seed=2)
    # algae_nbrs_2, crill_nbrs_2, fish_nbrs_2, shark_nbrs_2=run_update(pre_grid_2, iter=100, plot_number_of_species=False, return_numbers=True)

    # algae_diff=[np.abs(algae_1-algae_2) for algae_1, algae_2 in zip(algae_nbrs_1, algae_nbrs_2)]
    # crill_diff=[np.abs(crill_1-crill_2) for crill_1, crill_2 in zip(crill_nbrs_1, crill_nbrs_2)]
    # fish_diff=[np.abs(fish_1-fish_2) for fish_1, fish_2 in zip(fish_nbrs_1, fish_nbrs_2)]
    # shark_diff=[np.abs(shark_1-shark_2) for shark_1, shark_2 in zip(shark_nbrs_1, shark_nbrs_2)]

    # plt.figure()
    # plt.plot(algae_diff, 'g', label='Algae')
    # plt.plot(crill_diff, 'b', label='Crill')
    # plt.plot(fish_diff, 'r', label='Fish')
    # plt.plot(shark_diff, 'k', label='Shark')
    # plt.xlabel('iterations')
    # plt.ylabel('difference in number of species (different seeds)')
    # plt.legend()
    # plt.show()

    # tot_algae_nbrs=None
    # tot_crill_nbrs=None
    # tot_fish_nbrs=None
    # tot_shark_nbrs=None
    # nbr_of_seeds=20
    # for i in range(nbr_of_seeds):
    #     probabilities=[0.20, 0.20, 0.20, 0.20, 0.20]
    #     pre_grid=create_oscillation_with_four_grid(probabilities, seed=i+1)
    #     algae_nbrs, crill_nbrs, fish_nbrs, shark_nbrs=run_update(pre_grid, iter=100, plot_number_of_species=False, return_numbers=True)
    #     tot_algae_nbrs=algae_nbrs if tot_algae_nbrs is None else [tot_algae_nbr+algae_nbr for tot_algae_nbr, algae_nbr in zip(tot_algae_nbrs, algae_nbrs)]
    #     tot_crill_nbrs=crill_nbrs if tot_crill_nbrs is None else [tot_crill_nbr+crill_nbr for tot_crill_nbr, crill_nbr in zip(tot_crill_nbrs, crill_nbrs)]
    #     tot_fish_nbrs=fish_nbrs if tot_fish_nbrs is None else [tot_fish_nbr+fish_nbr for tot_fish_nbr, fish_nbr in zip(tot_fish_nbrs, fish_nbrs)]
    #     tot_shark_nbrs=shark_nbrs if tot_shark_nbrs is None else [tot_shark_nbr+shark_nbr for tot_shark_nbr, shark_nbr in zip(tot_shark_nbrs, shark_nbrs)]

    # mean_algae_nbrs=[tot_algae_nbr/nbr_of_seeds for tot_algae_nbr in tot_algae_nbrs]
    # mean_crill_nbrs=[tot_crill_nbr/nbr_of_seeds for tot_crill_nbr in tot_crill_nbrs]
    # mean_fish_nbrs=[tot_fish_nbr/nbr_of_seeds for tot_fish_nbr in tot_fish_nbrs]
    # mean_shark_nbrs=[tot_shark_nbr/nbr_of_seeds for tot_shark_nbr in tot_shark_nbrs]

    # plt.figure()
    # plt.plot(mean_algae_nbrs, 'g', label='Algae')
    # plt.plot(mean_crill_nbrs, 'b', label='Crill')
    # plt.plot(mean_fish_nbrs, 'r', label='Fish')
    # plt.plot(mean_shark_nbrs, 'k', label='Shark')
    # plt.xlabel('iterations')
    # plt.ylabel('number of species (mean over different seeds)')
    # plt.legend()
    # plt.show()

    # # Try to parallelize
    # tot_algae_nbrs=None
    # tot_crill_nbrs=None
    # tot_fish_nbrs=None
    # tot_shark_nbrs=None
    # nbr_of_seeds=50
    # iterations=1000
    # probabilities=[0.20, 0.19, 0.41, 0.20, 0]

    # # Creating the thread pool
    # with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
    #     # Submitting tasks to the thread pool
    #     futures = [executor.submit(get_numbers, i, iterations, probabilities) for i in range(nbr_of_seeds)]
    #     for future in concurrent.futures.as_completed(futures):
    #         algae_nbrs, crill_nbrs, fish_nbrs, shark_nbrs=future.result()
    #         tot_algae_nbrs=algae_nbrs if tot_algae_nbrs is None else [tot_algae_nbr+algae_nbr for tot_algae_nbr, algae_nbr in zip(tot_algae_nbrs, algae_nbrs)]
    #         tot_crill_nbrs=crill_nbrs if tot_crill_nbrs is None else [tot_crill_nbr+crill_nbr for tot_crill_nbr, crill_nbr in zip(tot_crill_nbrs, crill_nbrs)]
    #         tot_fish_nbrs=fish_nbrs if tot_fish_nbrs is None else [tot_fish_nbr+fish_nbr for tot_fish_nbr, fish_nbr in zip(tot_fish_nbrs, fish_nbrs)]
    #         tot_shark_nbrs=shark_nbrs if tot_shark_nbrs is None else [tot_shark_nbr+shark_nbr for tot_shark_nbr, shark_nbr in zip(tot_shark_nbrs, shark_nbrs)]

    # mean_algae_nbrs=[tot_algae_nbr/nbr_of_seeds for tot_algae_nbr in tot_algae_nbrs]
    # mean_crill_nbrs=[tot_crill_nbr/nbr_of_seeds for tot_crill_nbr in tot_crill_nbrs]
    # mean_fish_nbrs=[tot_fish_nbr/nbr_of_seeds for tot_fish_nbr in tot_fish_nbrs]
    # mean_shark_nbrs=[tot_shark_nbr/nbr_of_seeds for tot_shark_nbr in tot_shark_nbrs]

    # with open('seed_50_iter_1000_init_20_19_41_20_0.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)

    #     for i in range(len(mean_algae_nbrs)):
    #         writer.writerow([mean_algae_nbrs[i], mean_crill_nbrs[i], mean_fish_nbrs[i], mean_shark_nbrs[i]])


    data_orig = np.genfromtxt('seed_50_iter_1000_init_20_20_40_20_0.csv', delimiter=',', skip_header=1)
    data_change = np.genfromtxt('seed_50_iter_1000_init_20_19_41_20.csv', delimiter=',', skip_header=1)
    # Split the data into separate arrays (columns)
    mean_algae_nbrs1 = data_orig[:, 0]
    mean_crill_nbrs1 = data_orig[:, 1]
    mean_fish_nbrs1 = data_orig[:, 2]
    mean_shark_nbrs1 = data_orig[:, 3]

    mean_algae_nbrs2 = data_change[:, 0]
    mean_crill_nbrs2 = data_change[:, 1]
    mean_fish_nbrs2 = data_change[:, 2]
    mean_shark_nbrs2 = data_change[:, 3]

    plt.figure()
    plt.plot(mean_algae_nbrs1, 'g', label='Algae')
    plt.plot(mean_crill_nbrs1, 'b', label='Crill')
    plt.plot(mean_fish_nbrs1, 'r', label='Fish')
    plt.plot(mean_shark_nbrs1, 'k', label='Shark')
    plt.xlabel('iterations')
    plt.ylabel('number of species (mean over different seeds)')
    plt.legend()

    plt.figure()
    plt.plot(mean_algae_nbrs2, 'g', label='Algae')
    plt.plot(mean_crill_nbrs2, 'b', label='Crill')
    plt.plot(mean_fish_nbrs2, 'r', label='Fish')
    plt.plot(mean_shark_nbrs2, 'k', label='Shark')
    plt.xlabel('iterations')
    plt.ylabel('number of species (mean over different seeds)')
    plt.legend()
    plt.show()