import numpy
import random
from random import randint, random, sample, shuffle

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

def inSameCarrier(jetIdx1, jetIdx2, pilotIdx1, pilotIdx2):
    return (jetToCarrier[0][jetIdx1] == jetToCarrier[0][jetIdx2]
    == pilotToCarrier[0][pilotIdx1] == pilotToCarrier[0][pilotIdx2])

def inSameSquadron(jetIdx1, jetIdx2, pilotIdx1, pilotIdx2):
    return (jetToSquadron[0][jetIdx1] == jetToSquadron[0][jetIdx2]
    == pilotToSquadron[0][pilotIdx1] == pilotToSquadron[0][pilotIdx2])

def computeFitness(chromosome):
    avgSortieScore = 0
    for i in range(numSorties):
        offsetIdx = 4*i
        jetIdx1 = chromosome[offsetIdx + 0]
        jetIdx2 = chromosome[offsetIdx + 1]
        jetToJetScore = jetAffinity[jetIdx1][jetIdx2]
        pilotIdx1 = chromosome[offsetIdx + 2]
        pilotIdx2 = chromosome[offsetIdx + 3]
        pilotToPilotScore = pilotAffinity[pilotIdx1][pilotIdx2]
        pilotToJetScore = pilotJetAffinity[pilotIdx1][jetIdx1] + pilotJetAffinity[pilotIdx2][jetIdx2]

        # This is the score we want to minimize.
        # Affinity will roughly equate to if two entities are compatible
        # or are collocated (so smaller time or distance cost).
        avgSortieScore += (jetToJetScore + pilotToPilotScore + pilotToJetScore)

    # Don't spam the same jets/pilots over and over.
    numUniqueJets = len(set([chromosome[0], chromosome[1],
        chromosome[4], chromosome[5],
        chromosome[8], chromosome[9],
        chromosome[12], chromosome[13],
        chromosome[16], chromosome[17],
        chromosome[20], chromosome[21]]))
    if numSorties * 2 == numUniqueJets:
        avgSortieScore -= 100
    else:
        avgSortieScore += 500

    numUniquePilots = len(set([chromosome[2], chromosome[3],
        chromosome[6], chromosome[7],
        chromosome[10], chromosome[11],
        chromosome[14], chromosome[15],
        chromosome[18], chromosome[19],
        chromosome[22], chromosome[23]]))
    if numSorties * 2 == numUniquePilots:
        avgSortieScore -= 100
    else:
        avgSortieScore += 500

    return avgSortieScore / numSorties

def tournamentSelection(population, scores, k=25):
    # Pit k individuals against each other and select the best.
    selectionIdx = randint(0, len(population)-1)
    for i in range(0, k-1):
        idx = randint(0, len(population)-1)
        if scores[idx] < scores[selectionIdx]:
            selectionIdx = idx
    return population[selectionIdx]

def crossover(parent1, parent2, crossoverRate):
    # Create two kids from two parents.
    kid1, kid2 = parent1.copy(), parent2.copy()
    # Check for recombination chance.
    if random() < crossoverRate:
        # Swap sorties.
        kid1 = parent1[:12] + parent2[12:]
        kid2 = parent2[:12] + parent1[12:]
    return [kid1, kid2]

def mutation(chromosome, mutationRate):
    for i in range(len(chromosome)):
        if random() < mutationRate:
            # Flip the resource index to another random valid index.
            if i == 0 or i == 1:
                chromosome[i] = randint(0, numJets-1)
            elif i == 2 or i == 3:
                chromosome[i] = randint(0, numPilots-1)
            elif i == 4 or i == 5:
                chromosome[i] = randint(0, numJets-1)
            elif i == 6 or i == 7:
                chromosome[i] = randint(0, numPilots-1)
            elif i == 8 or i == 9:
                chromosome[i] = randint(0, numJets-1)
            elif i == 10 or i == 11:
                chromosome[i] = randint(0, numPilots-1)
            elif i == 12 or i == 13:
                chromosome[i] = randint(0, numJets-1)
            elif i == 14 or i == 15:
                chromosome[i] = randint(0, numPilots-1)
            elif i == 16 or i == 17:
                chromosome[i] = randint(0, numJets-1)
            elif i == 18 or i == 19:
                chromosome[i] = randint(0, numPilots-1)
            elif i == 20 or i == 21:
                chromosome[i] = randint(0, numJets-1)
            elif i == 22 or i == 23:
                chromosome[i] = randint(0, numPilots-1)

numSorties = 6
numJets = 19
numPilots = 21

# Create affinity matrices.
#
# So actually since we want to minimize our fitness cost,
# this is actually sort of reverse notion of affinity
# (lower score, more compatible).
#
# So also, ideally, these matrices aren't handcrafted and
# are figured out based on staff restrictions, squadron makeups, etc.
sameSquad = -24
sameCarrier = -12
costToMoveBetweenCarrier = 24
costOfWorkingRestriction = 50

jetAffinity = [[costToMoveBetweenCarrier] * numJets for i in range(numJets)]
reflectedFill(jetAffinity, range(0, 11), range(0, 11), sameCarrier)
reflectedFill(jetAffinity, range(11, 19), range(11, 19), sameCarrier)

reflectedFill(jetAffinity, range(0, 4), range(0, 4), sameSquad)
reflectedFill(jetAffinity, range(4, 8), range(4, 8), sameSquad)
reflectedFill(jetAffinity, range(8, 11), range(8, 11), sameSquad)
reflectedFill(jetAffinity, range(11, 15), range(11, 15), sameSquad)
reflectedFill(jetAffinity, range(15, 19), range(15, 19), sameSquad)

jetAffinity[9][10] = jetAffinity[10][9] = costOfWorkingRestriction

pilotAffinity = [[costToMoveBetweenCarrier] * numPilots for i in range(numPilots)]
reflectedFill(pilotAffinity, range(0, 14), range(0, 14), sameCarrier)
reflectedFill(pilotAffinity, range(14, 21), range(14, 21), sameCarrier)

reflectedFill(pilotAffinity, range(0, 5), range(0, 5), sameSquad)
reflectedFill(pilotAffinity, range(5, 10), range(5, 10), sameSquad)
reflectedFill(pilotAffinity, range(10, 14), range(10, 14), sameSquad)
reflectedFill(pilotAffinity, range(14, 17), range(14, 17), sameSquad)
reflectedFill(pilotAffinity, range(17, 21), range(17, 21), sameSquad)

pilotAffinity[0][1] = pilotAffinity[1][0] = costOfWorkingRestriction
pilotAffinity[10][11] = pilotAffinity[11][10] = costOfWorkingRestriction
# Should probably reverse this or check this in fitness cost.
# Having a lower cost here means the algo will want to spam these combos.
#pilotAffinity[2][3] = pilotAffinity[3][2] = costOfPreferentialAssignment
#pilotAffinity[2][8] = pilotAffinity[8][2] = costOfPreferentialAssignment
#pilotAffinity[17][20] = pilotAffinity[20][17] = costOfPreferentialAssignment
#pilotAffinity[17][18] = pilotAffinity[18][17] = costOfPreferentialAssignment

pilotJetAffinity = [[costToMoveBetweenCarrier] * numJets for i in range(numPilots)]
fill(pilotJetAffinity, range(0, 14), range(0, 11), sameCarrier)
fill(pilotJetAffinity, range(14, 21), range(11, 19), sameCarrier)

fill(pilotJetAffinity, range(0, 5), range(0, 4), sameSquad)
fill(pilotJetAffinity, range(5, 10), range(4, 8), sameSquad)
fill(pilotJetAffinity, range(10, 14), range(8, 11), sameSquad)
fill(pilotJetAffinity, range(14, 17), range(11, 15), sameSquad)
fill(pilotJetAffinity, range(17, 21), range(15, 19), sameSquad)

pilotToCarrier = [[0] * numPilots for i in range(1)]
fill(pilotToCarrier, range(1), range(0, 14), 0)
fill(pilotToCarrier, range(1), range(14, 21), 1)

pilotToSquadron = [[0] * numPilots for i in range(1)]
fill(pilotToCarrier, range(1), range(0, 5), 0)
fill(pilotToCarrier, range(1), range(5, 10), 1)
fill(pilotToCarrier, range(1), range(10, 14), 2)
fill(pilotToCarrier, range(1), range(15, 17), 3)
fill(pilotToCarrier, range(1), range(17, 21), 4)

jetToCarrier = [[0] * numJets for i in range(1)]
fill(jetToCarrier, range(1), range(0, 11), 0)
fill(jetToCarrier, range(1), range(11, 19), 1)

jetToSquadron = [[0] * numJets for i in range(1)]
fill(pilotToCarrier, range(1), range(0, 4), 0)
fill(pilotToCarrier, range(1), range(4, 8), 1)
fill(pilotToCarrier, range(1), range(9, 11), 2)
fill(pilotToCarrier, range(1), range(11, 15), 3)
fill(pilotToCarrier, range(1), range(15, 19), 4)

numPopulation = 1000
# 2 pilots, 2 jets
numGenes = numSorties * 4
numGenerations = 50
# This is supposed to be relatively high.
crossoverRate = .99
# This is supposed to be relatively low.
mutationRate = .12

# Defining the population size.
# The population will have n chromosomes where each chromosome has m genes.
populationSize = (numPopulation, numGenes)

#Creating the initial population.
population = []
for i in range(numPopulation):
    newChromosome = []
    for i in range(numSorties):
        newChromosome += sample(range(0, numJets), 2)
        newChromosome += sample(range(0, numPilots), 2)
    population.append(newChromosome)

best, best_eval = 0, computeFitness(population[0])
for genIdx in range(numGenerations):
    # Compute fitness of all candidate chromosomes.
    scores = [computeFitness(c) for c in population]
    #print (scores)

    # Check for new best.
    for i in range(numPopulation):
        if scores[i] < best_eval:
            best, best_eval = population[i], scores[i]
            print(">%d, new best f(%s) = %.3f" % (genIdx,  population[i], scores[i]))

    # Select parents.
    selected = [tournamentSelection(population, scores) for _ in range(numPopulation)]
    #print (selected)

    # Create the next generation from the parents.
    children = list()
    for i in range(0, numPopulation, 2):
        parent1, parent2 = selected[i], selected[i+1]
        for child in crossover(parent1, parent2, crossoverRate):
            mutation(child, mutationRate)
            children.append(child)
    population = children

print(best)
print(best_eval)