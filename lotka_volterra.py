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

    dxdt_1 = -x[0]*x[1] + x[3]*x[3]
    dxdt_2 = x[0]*x[1] - x[1]*x[1] - x[1]*x[2] - x[1]*x[3]
    dxdt_3 = 0.01*x[0]*x[0] + 0.01*x[1]*x[2] + 0.01*x[1]*x[3] - x[2]*x[3]
    dxdt_4 = 0.01*x[2]*x[3] - x[3]*x[3]
    return [dxdt_1, dxdt_2, dxdt_3, dxdt_4]


def plot_lotka_volterra():
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
    plt.plot(solution.t, solution.y[1], label='Crill Population', color='blue')
    plt.plot(solution.t, solution.y[2], label='Fish Population', color='red')
    plt.plot(solution.t, solution.y[3], label='Shark Population', color='black')
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

    #Attempt at chaos:
    r = np.array([1, 0.42, 0.57, 0.72])  # Varied growth rates
    s=1
    A = np.array([[-1, -0.06*s,  -2.2*s,  -0.5*s],
                    [-0.42*0.36*s,  -0.42, -0.42*0.05*s,  -0.42*1.32*s],
                    [- 0.57*1.41*s,  -0.57*1.07*s,  -0.57, -0.57*0.17*s],
                    [- 0.72*0.26*s,  - 0.72*0.54*s,  - 0.72*1.15*s,  - 0.72]])
    x0 = np.array([0.1102, 0.443, 0.305, 0.38])

        # Time span over which we want to solve the system
    t_span = (0, 1500)  # From time t=0 to t=50
    t_eval = np.linspace(t_span[0], t_span[1], 15000)  # Points at which we evaluate

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
    plt.title('Attempt at chaos:')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    plot_lotka_volterra()