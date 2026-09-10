from math import cos
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import pandas as pd

# solver settings
a = 0.8 # infection
g = 0.2 # recovery
X_o = [0.95, 0.05, 0] # initial compartment amounts (S, I, R)
t_span = (0, 30) # time span
max_step = 0.1 # largest step size solver will use

# some graphing settings + more!
csv_file_name = "sirs_solution.csv"
graph_title = "SIRS Model"
graph_subtitle = fr"$\alpha$ = {a}, $\beta$ = oscillatory, $\gamma$ = {g}, Initial Conditions: S = {X_o[0]}, I = {X_o[1]}, R = {X_o[2]}"
x_axis_name = "Time"
y_axis_name = "Population Fraction"
y1_data_name = "Susceptible"
y2_data_name = "Infected"
y3_data_name = "Recovered"

def b(t):
    return 0.25 * cos(t) + 0.25

def ode_system(t, state):
    global a, g
    S, I, R = state
    dSdt = -a * S * I + b(t) * R
    dIdt = -g * I + a * S * I
    dRdt = -b(t) * R + g * I
    return [dSdt, dIdt, dRdt]

solution = solve_ivp(ode_system, t_span, X_o, max_step=max_step)

print(f"Solver Passed: {solution.success}")
print(solution.message)

results = pd.DataFrame({
    x_axis_name : solution.t,
    y1_data_name : solution.y[0],
    y2_data_name : solution.y[1],
    y3_data_name : solution.y[2],
})

results.to_csv(csv_file_name, index=False)
print(f"{csv_file_name} has been saved!")

plt.figure(figsize=[12, 9])

plt.rcParams.update({'font.size': 25})
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.size'] = 8
plt.rcParams['ytick.major.size'] = 8
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2
plt.rcParams['xtick.minor.size'] = 6
plt.rcParams['ytick.minor.size'] = 6
plt.rcParams['xtick.minor.width'] = 2
plt.rcParams['ytick.minor.width'] = 2
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams['axes.linewidth'] = 2

plt.plot(solution.t, solution.y[0], label=y1_data_name)
plt.plot(solution.t, solution.y[1], label=y2_data_name)
plt.plot(solution.t, solution.y[2], label=y3_data_name)

plt.xlim(t_span[0], t_span[1])
plt.ylim(0, 1)

plt.suptitle(graph_title)
plt.title(graph_subtitle, fontsize=20, pad=15)
plt.xlabel(x_axis_name)
plt.ylabel(y_axis_name)

plt.legend()
plt.grid()

plt.savefig(graph_title.replace(" ", "") + ".png")
print(f"Graph {graph_title.replace(" ", "")}.png has been saved!")

plt.show()