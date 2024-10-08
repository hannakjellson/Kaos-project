import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def lotka_volterra(r, A):
    pass

# Havs-ekosystemet
def dxdt(t, x, r, A):
    D_x = np.diag(x)  # Create the diagonal matrix D(x)
    return D_x @ (r + A @ x)  # Equivalent to D(x) * (r + A * x)

# Agarplattan:
def dxdtAgar(t, x):
    # x[0] = Algae, x[1] = Krill, x[2] = Fish, x[3] = Shark
    
    # Growth rates and interaction coefficients (hard-coded)
    growth_algae = 0.5  # Growth rate for Algae
    growth_krill = -0.5  # Natural decline for Krill
    growth_fish = -0.5  # Natural decline for Fish
    growth_shark = -0.5  # Natural decline for Sharks

    # Interaction terms
    interaction_krill_algae = 0.1  # Krill benefit from Algae
    interaction_algae_krill = -0.1  # Algae is eaten by Krill
    
    interaction_fish_krill = 0.1  # Fish benefit from eating Krill
    interaction_krill_fish = -0.1  # Krill is eaten by Fish
    
    interaction_shark_fish = 0.1  # Sharks benefit from eating Fish
    interaction_fish_shark = -0.1  # Fish is eaten by Sharks
    '''
    # Differential equations for each species
    dxdt_1 = x[0] * (growth_algae + interaction_algae_krill * x[1])  # Algae population equation
    dxdt_2 = x[1] * (growth_krill + interaction_krill_algae * x[0] + interaction_krill_fish * x[2])  # Krill population equation
    dxdt_3 = x[2] * (growth_fish + interaction_fish_krill * x[1] + interaction_fish_shark * x[3])  # Fish population equation
    dxdt_4 = x[3] * (growth_shark + interaction_shark_fish * x[2])  # Shark population equation
    '''
    dxdt_1 = -x[0]*x[1] + x[3]*x[3]
    dxdt_2 = x[0]*x[1] - x[1]*x[1] - x[1]*x[2] - x[1]*x[3]
    dxdt_3 = 0.01*x[0]*x[0] + 0.01*x[1]*x[2] + 0.01*x[1]*x[3] - x[2]*x[3]
    dxdt_4 = 0.01*x[2]*x[3] - x[3]*x[3]
    return [dxdt_1, dxdt_2, dxdt_3, dxdt_4]



if __name__ == '__main__':

    # Parameters
    r = np.array([0.5, -0.5, -0.5, -0.5])  # Growth rates for each species
    A = np.array([[0.0, -0.1, 0, 0],  # Interaction matrix (prey-predator type)
                [0.1, 0.0, -0.1, 0],
                [0, 0.1, 0, -0.1],
                [0, 0, 0.1, 0]])

    # Initial condition for populations at t=0 (prey and predator)
    x0 = np.array([10, 5, 6, 7])

    # Time span over which we want to solve the system
    t_span = (0, 50)  # From time t=0 to t=50
    t_eval = np.linspace(t_span[0], t_span[1], 500)  # Points at which we evaluate

    # Solve the system of ODEs
    solution = solve_ivp(dxdt, t_span, x0, args=(r, A), t_eval=t_eval, vectorized=False)

    # Plotting the solution
    plt.plot(solution.t, solution.y[0], label='Algea Population', color='green')
    plt.plot(solution.t, solution.y[1], label='Crill Population', color='orange')
    plt.plot(solution.t, solution.y[2], label='Fish Population', color='yellow')
    plt.plot(solution.t, solution.y[3], label='Shark Population', color='blue')
    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.legend()
    plt.title('Numerical Solution of the Nonlinear System')
    plt.grid(True)
    plt.show()

    # Agarplattan:



    # Initial condition for populations at t=0 (prey and predator)
    x0 = np.array([10, 5, 6, 7])  # Initial populations: [Algae, Krill, Fish, Sharks]

    # Time span over which we want to solve the system
    t_span = (0, 50)  # From time t=0 to t=50
    t_eval = np.linspace(t_span[0], t_span[1], 2000)  # Points at which we evaluate

    # Solve the system of ODEs
    solution = solve_ivp(dxdtAgar, t_span, x0, t_eval=t_eval, vectorized=False)

    # Plotting the solution
    plt.plot(solution.t, solution.y[0], label='Agar Population', color='green')
    plt.plot(solution.t, solution.y[1], label='Bacteria Population', color='orange')
    plt.plot(solution.t, solution.y[2], label='Amoeba Population', color='yellow')
    plt.plot(solution.t, solution.y[3], label='Waste Population', color='blue')
    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.legend()
    plt.title('Numerical Solution of Lotka-Volterra equations')
    plt.grid(True)
    plt.show()

