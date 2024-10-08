import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def lotka_volterra(r, A):
    pass

# Lotka-Volterra
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
    '''
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
    t_eval = np.linspace(t_span[0], t_span[1], 20000)  # Points at which we evaluate

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
    '''

    '''
    #- - - - - - - - - - De 4 elementen - - - - - - - - - - - - - - - - - -
    # Parameters
    alpha = 0.1
    beta = 0.1
    r = np.array([0, 0, 0, 0])  # Growth rates for each species
    A = np.array([[0.0, beta, 0, -alpha],  # Interaction matrix (prey-predator type)
                [-alpha, 0, beta, 0],
                [0, -alpha, 0, beta],
                [beta, 0, -alpha, 0]])

    # Initial condition for populations at t=0 (prey and predator)
    x0 = np.array([11, 2, 6, 7])

    for i in range(0,10):

        x0 = np.array([11, 2 + i*0.01, 6, 7])
        # Time span over which we want to solve the system
        t_span = (0, 500)  # From time t=0 to t=50
        t_eval = np.linspace(t_span[0], t_span[1], 5000)  # Points at which we evaluate

        # Solve the system of ODEs
        solution = solve_ivp(dxdt, t_span, x0, args=(r, A), t_eval=t_eval, vectorized=False)

        # Plotting the solution
        plt.plot(solution.t, solution.y[0], label='Fire Population', color='red')
        plt.plot(solution.t, solution.y[1], label='Earth Population', color='green')
        plt.plot(solution.t, solution.y[2], label='Water Population', color='blue')
        plt.plot(solution.t, solution.y[3], label='Wind Population', color='orange')
        plt.xlabel('Time')
        plt.ylabel('Population')
        plt.legend()
        plt.title('Numerical Solution of the Nonlinear System')
        plt.grid(True)
        plt.show()
    '''


    '''
    for i in range(10):
        # Adjust initial conditions slightly for each run
        x0 = np.array([11, 2 + i * 0.01, 6, 7])
        
            # Initialize solve_ivp with stepwise integration
    solver = solve_ivp(dxdt, t_span, x0, args=(r, A), dense_output=True, vectorized=False)

    # Empty arrays to store the constrained solutions
    t_values = []
    y_values = []

    # Step through the solution manually
    while solver.status == 'running':
        solver.step()  # Take a step in the integration

        # Enforce the constraint on the current solution
        constrained_y = enforce_constraint(solver.y, constant)

        # Store the constrained solution
        t_values.append(solver.t)
        y_values.append(constrained_y)

    # Convert lists to arrays for plotting
    t_values = np.array(t_values)
    y_values = np.array(y_values).T  # Transpose for plotting

    # Plot the results
    plt.plot(t_values, y_values[0], label='Fire Population', color='red')
    plt.plot(t_values, y_values[1], label='Earth Population', color='green')
    plt.plot(t_values, y_values[2], label='Water Population', color='blue')
    plt.plot(t_values, y_values[3], label='Wind Population', color='orange')

    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.legend()
    plt.title('Numerical Solution with Manifold Projection (Stepwise Integration)')
    plt.grid(True)
    plt.show()
    '''

    #Manifold method
    # Parameters
    alpha = 0.1
    beta = 0.1
    r = np.array([0, 0, 0, 0])
    A = np.array([[0.0, beta, 0, -alpha],
                [-alpha, 0, beta, 0],
                [0, -alpha, 0, beta],
                [beta, 0, -alpha, 0]])


    # Projection function to enforce the constraint
    def enforce_constraint(x, constant):
        current_total = np.sum(x)
        # Calculate the difference
        diff = current_total - constant

        # Distribute the difference evenly among all species
        adjustment = diff / len(x)  # Assuming len(x) is 4 (i.e., x[0], x[1], x[2], x[3])
        
        # Apply the adjustment
        x += -adjustment  # Subtract the adjustment from each species
        return x



    # Time span for integration
    t_span = (0, 500)
    #t_eval = np.linspace(t_span[0], t_span[1], 5000)

    for i in range(10):
        # Adjust initial conditions slightly for each run
        x0 = np.array([11, 2 + i * 0.01, 6 - i*0.01, 7])
        constant = np.sum(x0)  # The sum of x[0] + x[1] + x[2] + x[3]
        
        # Initialize solve_ivp with dense_output=True
        solver = solve_ivp(dxdt, t_span, x0, args=(r, A), dense_output=True, vectorized=False)

        # Empty arrays to store the constrained solutions
        t_values = []
        y_values = []

        # Time array for the dense output
        t_eval = np.linspace(t_span[0], t_span[1], 5000)

        # Step through the solution manually
        for t in t_eval:
            # Get the current solution
            solver.t = t
            solver.y = solver.sol(t)

            # Enforce the constraint on the current solution
            constrained_y = enforce_constraint(solver.y, constant)

            # Store the constrained solution
            t_values.append(t)
            y_values.append(constrained_y)

        # Convert lists to arrays for plotting
        t_values = np.array(t_values)
        y_values = np.array(y_values).T  # Transpose for plotting

        # Check if y_values is empty
        if y_values.size == 0:
            print(f"No data to plot for iteration {i}.")
            continue

        # Create subplots
        fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

        # Plot individual populations
        axs[0].plot(t_values, y_values[0], label='Fire Population', color='red')
        axs[0].plot(t_values, y_values[1], label='Earth Population', color='green')
        axs[0].plot(t_values, y_values[2], label='Water Population', color='blue')
        axs[0].plot(t_values, y_values[3], label='Wind Population', color='orange')

        axs[0].set_ylabel('Population')
        axs[0].legend()
        axs[0].set_title(f'Populations of Species (i={i})')
        axs[0].grid(True)

        # Calculate and plot the sum of populations
        total_population = np.sum(y_values, axis=0)
        axs[1].plot(t_values, total_population, label='Total Population', color='purple')

        axs[1].set_xlabel('Time')
        axs[1].set_ylabel('Total Population')
        axs[1].legend()
        axs[1].set_title('Total Population of All Species')
        axs[1].grid(True)

        # Show the plots
        plt.tight_layout()
        plt.show()

        '''

        # Plot the results
        plt.plot(t_values, y_values[0], label='Fire Population', color='red')
        plt.plot(t_values, y_values[1], label='Earth Population', color='green')
        plt.plot(t_values, y_values[2], label='Water Population', color='blue')
        plt.plot(t_values, y_values[3], label='Wind Population', color='orange')

        plt.xlabel('Time')
        plt.ylabel('Population')
        plt.legend()
        plt.title(f'Numerical Solution with Manifold Projection (i={i})')
        plt.grid(True)
        plt.show()

        '''

if __name__ == '__main__':
    plot_lotka_volterra()