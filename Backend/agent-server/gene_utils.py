from random import randint

def getUniqueCombos(dim1, dim2):
    unique_combinations = [(dim1[i], dim2[j]) for i in range(len(dim1)) for j in range(len(dim2))]
    return unique_combinations

def reflectedFill(matrix, dim1, dim2, value):
    combos = getUniqueCombos(dim1, dim2)
    for combo in combos:
        if combo[0] != combo[1]:
            matrix[combo[0]][combo[1]] = matrix[combo[1]][combo[0]] = value

def fill(matrix, dim1, dim2, value):
    for i in dim1:
        for j in dim2:
            matrix[i][j] = value

def tournamentSelection(population, scores, k=25):
    # Pit k individuals against each other and select the best.
    selectionIdx = randint(0, len(population)-1)
    for i in range(0, k-1):
        idx = randint(0, len(population)-1)
        if scores[idx] < scores[selectionIdx]:
            selectionIdx = idx
    return population[selectionIdx]
