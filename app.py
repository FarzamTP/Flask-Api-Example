import numpy as np
from flask import Flask
from flask import request
from flask import jsonify
from scipy.optimize import linprog
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable, LpMinimize

app = Flask(__name__)


# ================================== Maximization LP ================================

@app.route('/solve_max', methods=['POST', 'GET'])
def maximize_problem_solve():
    # Define the model
    model = LpProblem(name="resource-allocation", sense=LpMaximize)

    # Define the decision variables
    x = {i: LpVariable(name=f"x{i}", lowBound=0) for i in range(1, 5)}

    # Add constraints
    model += (lpSum(x.values()) <= 50, "manpower")
    model += (3 * x[1] + 2 * x[2] + x[3] <= 100, "material_a")
    model += (x[2] + 2 * x[3] + 3 * x[4] <= 90, "material_b")

    # Set the objective
    model += 20 * x[1] + 12 * x[2] + 40 * x[3] + 25 * x[4]

    # Solve the optimization problem
    status = model.solve()

    # Get the results
    print(f"status: {model.status}, {LpStatus[model.status]}")
    print(f"objective: {model.objective.value()}")

    variables = {}
    constants = {}

    for var in x.values():
        print(f"{var.name}: {var.value()}")
        variables[str(var.name)] = var.value()

    for name, constraint in model.constraints.items():
        print(f"{name}: {constraint.value()}")
        constants[str(name)] = constraint.value()

    print(variables)
    print(constants)

    return {"status": str(model.status) + ", " + str(LpStatus[model.status]),
            "optimum-value": model.objective.value(),
            "variables-opt-value": variables,
            "constants-value": constants}


# ================================== Minimization LP ================================

@app.route('/solve_min', methods=['POST', 'GET'])
def minimize_problem_solve():
    # Initialize Class
    model = LpProblem("Minimize Staffing", LpMinimize)
    days = list(range(7))
    # Define Decision Variables
    x = LpVariable.dicts('staff_', days, lowBound=0, cat='Integer')
    # Def1ine Objective
    model += lpSum([x[i] for i in days])
    model += (x[0] + x[3] + x[4] + x[5] + x[6] >= 11, "C1")
    model += (x[0] + x[1] + x[4] + x[5] + x[6] >= 14, "C2")
    model += (x[0] + x[1] + x[2] + x[5] + x[6] >= 23, "C3")
    model += (x[0] + x[1] + x[2] + x[3] + x[6] >= 21, "C4")
    model += (x[0] + x[1] + x[2] + x[3] + x[4] >= 20, "C5")
    model += (x[1] + x[2] + x[3] + x[4] + x[5] >= 15, "C6")
    model += (x[2] + x[3] + x[4] + x[5] + x[6] >= 8, "C7")

    # Solve Model
    model.solve()

    # Get the results
    print(f"status: {model.status}, {LpStatus[model.status]}")
    print(f"objective: {model.objective.value()}")

    variables = {}
    constants = {}

    for var in x.values():
        print(f"{var.name}: {var.value()}")
        variables[str(var.name)] = var.value()

    for name, constraint in model.constraints.items():
        print(f"{name}: {constraint.value()}")
        constants[str(name)] = constraint.value()

    return {"status": str(model.status) + ", " + str(LpStatus[model.status]),
            "optimum-value": model.objective.value(),
            "variables-opt-value": variables,
            "constants-value": constants}


if __name__ == '__main__':
    app.run()
