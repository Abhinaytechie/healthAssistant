from ortools.sat.python import cp_model

model = cp_model.CpModel()
x = model.NewIntVar(0, 10, "x")
model.Add(x <= 5)

solver = cp_model.CpSolver()
status = solver.Solve(model)

print("Solver status:", status)       # Expect 4 = OPTIMAL
print("Value of x:", solver.Value(x)) # Expect 5
