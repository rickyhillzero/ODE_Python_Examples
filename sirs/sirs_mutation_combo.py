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
csv_file_name = "sirs_solution_combo.csv"
graph_title = "SIRS Combo"
graph_subtitle = fr"$\alpha$ = {a}, $\gamma$ = {g}, Initial Conditions: S = {X_o[0]}, I = {X_o[1]}, R = {X_o[2]}"
x_axis_name = "Time"
y_axis_name = "Population Fraction"
y1_data_name = "Susceptible"
y2_data_name = "Infected"
y3_data_name = "Recovered"

def b(t, bool):
    if bool:
        return 0.25 * cos(t) + 0.25
    return 0.1

def ode_system(t, state):
    global a, g
    S, I, R = state
    dSdt = -a * S * I + b(t, False) * R
    dIdt = -g * I + a * S * I
    dRdt = -b(t, False) * R + g * I
    return [dSdt, dIdt, dRdt]

def ode_system_mutate(t, state):
    global a, g
    S, I, R = state
    dSdt = -a * S * I + b(t, True) * R
    dIdt = -g * I + a * S * I
    dRdt = -b(t, True) * R + g * I
    return [dSdt, dIdt, dRdt]

solution = solve_ivp(ode_system, t_span, X_o, max_step=max_step)
print(f"Solver Passed: {solution.success}")
print(solution.message)

solution_mutate = solve_ivp(ode_system_mutate, t_span, X_o, max_step=max_step)
print(f"Solver Passed: {solution.success}")
print(solution.message)

results = pd.DataFrame({
    x_axis_name : solution.t,
    y1_data_name : solution.y[0],
    y2_data_name : solution.y[1],
    y3_data_name : solution.y[2],
    y1_data_name + "_m" : solution_mutate.y[0],
    y2_data_name + "_m" : solution_mutate.y[1],
    y3_data_name + "_m" : solution_mutate.y[2],
})

results.to_csv(csv_file_name, index=False)
print(f"{csv_file_name} has been saved!")

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

fig, ax = plt.subplots(1,2, figsize=[15, 9])
fig.subplots_adjust(wspace=0.5)

fig.suptitle(graph_title)
fig.text(0.5, 0.01, graph_subtitle, fontsize=15, va="center", ha="center")

ax0 = ax[0]
ax0.plot(solution.t, solution.y[0], label=y1_data_name)
ax0.plot(solution.t, solution.y[1], label=y2_data_name)
ax0.plot(solution.t, solution.y[2], label=y3_data_name)
ax0.set_title("SIRS", fontsize=20, pad=15)
ax0.text(23, -0.1, fr"$\beta = {b(0, False)}$", fontsize=15, ha="center", va="center")
ax0.axis('on')
ax0.set_xlabel(x_axis_name)
ax0.set_ylabel(y_axis_name)
ax0.set_xlim(t_span[0], t_span[1])
ax0.set_ylim(0, 1)
ax0.legend()
ax0.grid()

ax1 = ax[1]
ax1.plot(solution.t, solution_mutate.y[0], label=y1_data_name)
ax1.plot(solution.t, solution_mutate.y[1], label=y2_data_name)
ax1.plot(solution.t, solution_mutate.y[2], label=y3_data_name)
ax1.set_title("SIRS Mutate", fontsize=20, pad=15)
ax1.text(24.5, -0.1, r"$\beta = 0.25\cos{t}+0.25$", fontsize=15, ha="center", va="center")
ax1.axis('on')
ax1.set_xlabel(x_axis_name)
ax1.set_ylabel(y_axis_name)
ax1.set_xlim(t_span[0], t_span[1])
ax1.set_ylim(0, 1)
ax1.legend()
ax1.grid()

plt.savefig(graph_title.replace(" ", "") + ".png")
print(f"Graph {graph_title.replace(" ", "")}.png has been saved!")

plt.tight_layout()
plt.show()