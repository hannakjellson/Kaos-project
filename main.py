import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def lotka_volterra(r, A):
    pass



if __name__ == '__main__':
    r = np.array([[1],[2]])
    A = np.array([[2,3],[4,12]])
    print(r)
    print(A)
    print(A@r)
    #lotka_volterra()


    # Define the system of ODEs
    def dxdt(t, x, r, A):
        D_x = np.diag(x)  # Create the diagonal matrix D(x)
        return D_x @ (r + A @ x)  # Equivalent to D(x) * (r + A * x)

    # Parameters
    r = np.array([0.5, -0.5])  # Growth rates for each species
    A = np.array([[0.0, -0.1],  # Interaction matrix (prey-predator type)
                [0.1, 0.0]])

    # Initial condition for populations at t=0 (prey and predator)
    x0 = np.array([10, 5])

    # Time span over which we want to solve the system
    t_span = (0, 50)  # From time t=0 to t=50
    t_eval = np.linspace(t_span[0], t_span[1], 500)  # Points at which we evaluate

    # Solve the system of ODEs
    solution = solve_ivp(dxdt, t_span, x0, args=(r, A), t_eval=t_eval, vectorized=False)

    # Plotting the solution
    plt.plot(solution.t, solution.y[0], label='Prey Population (x1)', color='blue')
    plt.plot(solution.t, solution.y[1], label='Predator Population (x2)', color='orange')
    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.legend()
    plt.title('Numerical Solution of the Nonlinear System')
    plt.grid(True)
    plt.show()
