import itertools
from ortools.linear_solver import pywraplp

def AllocateJetPairsToTargets(vehicleIds, minJetsPerSortie,
    targetTimeConstraints, targetIds, targetIdxSequence):

    # Create the cost matrix. For starters, this will be
    # numCombos-by-numTargets and the cost will simply be the max sortie time
    # for the target. Maybe to make things interesting we could vary cost
    # by whether it meets sortie size limits, jet combo restrictions, etc.
    costMatrix = []
    for i in range(0, len(vehicleIds)):
        costRow = []
        for targetIdx in targetIdxSequence:
            targetId = targetIds[targetIdx]
            foundTimeConstraint = next((x for x in targetTimeConstraints if x['id'] == targetId), None)
            if (foundTimeConstraint):
                costRow.append(foundTimeConstraint['maxSortieTime'])
        costMatrix.append(costRow)
    
    num_pairs = len(vehicleIds)
    num_tasks = len(costMatrix[0])

    # Solver
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    # x[i, j] is an array of 0-1 variables, which will be 1
    # if pair i is assigned to task j.
    x = {}
    for i in range(num_pairs):
        for j in range(num_tasks):
            x[i, j] = solver.IntVar(0, 1, '')

    # Constraints
    # Each jet is assigned to at most n tasks.
    for i in range(num_pairs):
        solver.Add(solver.Sum([x[i, j] for j in range(num_tasks)]) <= 3)

    # Each task is assigned to exactly n jets.
    for j in range(num_tasks):
        solver.Add(solver.Sum([x[i, j] for i in range(num_pairs)]) == minJetsPerSortie)

    
    # Objective
    objective_terms = []
    for i in range(num_pairs):
        for j in range(num_tasks):
            objective_terms.append(costMatrix[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    # Solve
    status = solver.Solve()

    # Print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print('Total cost = ', solver.Objective().Value(), '\n')
        for i in range(num_pairs):
            for j in range(num_tasks):
                # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                if x[i, j].solution_value() > 0.5:
                    print('Pair %s assigned to task %d.  Cost = %d' %
                          (vehicleIds[i], j, costMatrix[i][j]))

