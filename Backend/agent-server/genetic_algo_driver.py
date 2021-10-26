import itertools
import numpy
import random
from random import randint, random, sample

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

def computeFitness(chromosome):
    jetIdx1 = chromosome[0]
    jetIdx2 = chromosome[1]
    jetToJetScore = jetAffinity[jetIdx1][jetIdx2]
    pilotIdx1 = chromosome[2]
    pilotIdx2 = chromosome[3]
    pilotToPilotScore = pilotAffinity[pilotIdx1][pilotIdx2]
    pilotToJetScore = pilotJetAffinity[pilotIdx1][jetIdx1] + pilotJetAffinity[pilotIdx2][jetIdx2]
    missileIdx1 = chromosome[4]
    missileIdx2 = chromosome[5]
    missileToJetScore = missileJetAffinity[missileIdx1][jetIdx1] + missileJetAffinity[missileIdx2][jetIdx2]
    missileToPilotScore = missilePilotAffinity[missileIdx1][pilotIdx1] + missilePilotAffinity[missileIdx2][pilotIdx2]

    # This is the score we want to minimize.
    # Affinity will roughly equate to if two entities are compatible
    # or are collocated (so smaller time or distance cost).
    score = (jetToJetScore + pilotToPilotScore + pilotToJetScore + missileToJetScore + missileToPilotScore)
    return score

def tournamentSelection(population, scores, k=200):
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
        # Select a random crossover point.
        crossPointIdx = randint(1, len(parent1)-2)
        # Perform crossover (literally swap genes).
        kid1 = numpy.concatenate((parent1[:crossPointIdx], parent2[crossPointIdx:]))
        kid2 = numpy.concatenate((parent2[:crossPointIdx], parent1[crossPointIdx:]))
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
                chromosome[i] = randint(0, numMissiles-1)

numJets = 19
numPilots = 21
numMissiles = 13

# Create affinity matrices.
#
# So actually since we want to minimize our fitness cost,
# this is actually sort of reverse notion of affinity
# (lower score, more compatible).
#
# So also, ideally, these matrices aren't handcrafted and
# are figured out based on staff restrictions, squadron makeups, etc.
baseCost = -5
costOfPreferentialAssignment = -100
costToMoveBetweenCarrier = 24
costOfWorkingRestriction = 50

jetAffinity = [[costToMoveBetweenCarrier] * numJets for i in range(numJets)]
reflectedFill(jetAffinity, range(0, 4), range(0, 4), baseCost)
reflectedFill(jetAffinity, range(4, 8), range(4, 8), baseCost)
reflectedFill(jetAffinity, range(8, 11), range(8, 11), baseCost)
reflectedFill(jetAffinity, range(11, 15), range(11, 15), baseCost)
reflectedFill(jetAffinity, range(15, 19), range(15, 19), baseCost)
jetAffinity[9][10] = jetAffinity[10][9] = costOfWorkingRestriction

pilotAffinity = [[costToMoveBetweenCarrier] * numPilots for i in range(numPilots)]
reflectedFill(pilotAffinity, range(0, 5), range(0, 5), baseCost)
reflectedFill(pilotAffinity, range(5, 10), range(5, 10), baseCost)
reflectedFill(pilotAffinity, range(10, 14), range(10, 14), baseCost)
reflectedFill(pilotAffinity, range(14, 17), range(14, 17), baseCost)
reflectedFill(pilotAffinity, range(17, 21), range(17, 21), baseCost)
pilotAffinity[0][1] = pilotAffinity[1][0] = costOfWorkingRestriction
pilotAffinity[10][11] = pilotAffinity[11][10] = costOfWorkingRestriction
pilotAffinity[2][3] = pilotAffinity[3][2] = costOfPreferentialAssignment
pilotAffinity[2][8] = pilotAffinity[8][2] = costOfPreferentialAssignment
pilotAffinity[17][20] = pilotAffinity[20][17] = costOfPreferentialAssignment
pilotAffinity[17][18] = pilotAffinity[18][17] = costOfPreferentialAssignment

pilotJetAffinity = [[costToMoveBetweenCarrier] * numJets for i in range(numPilots)]
fill(pilotJetAffinity, range(0, 5), range(0, 4), baseCost)
fill(pilotJetAffinity, range(5, 10), range(4, 8), baseCost)
fill(pilotJetAffinity, range(10, 14), range(8, 11), baseCost)
fill(pilotJetAffinity, range(14, 17), range(11, 15), baseCost)
fill(pilotJetAffinity, range(17, 21), range(15, 19), baseCost)

missileAffinity = [[costToMoveBetweenCarrier] * numMissiles for i in range(numMissiles)]
reflectedFill(pilotAffinity, range(0, 2), range(0, 2), baseCost)
reflectedFill(pilotAffinity, range(2, 5), range(2, 5), baseCost)
reflectedFill(pilotAffinity, range(5, 8), range(5, 8), baseCost)
reflectedFill(pilotAffinity, range(8, 11), range(8, 11), baseCost)
reflectedFill(pilotAffinity, range(11, 13), range(11, 13), baseCost)

missilePilotAffinity = [[costToMoveBetweenCarrier] * numPilots for i in range(numMissiles)]
fill(missilePilotAffinity, range(0, 2), range(0, 5), baseCost)
fill(missilePilotAffinity, range(2, 5), range(5, 10), baseCost)
fill(missilePilotAffinity, range(5, 8), range(10, 14), baseCost)
fill(missilePilotAffinity, range(8, 11), range(14, 17), baseCost)
fill(missilePilotAffinity, range(11, 13), range(17, 21), baseCost)

missileJetAffinity = [[costToMoveBetweenCarrier] * numJets for i in range(numMissiles)]
fill(missileJetAffinity, range(0, 2), range(0, 4), baseCost)
fill(missileJetAffinity, range(2, 5), range(4, 8), baseCost)
fill(missileJetAffinity, range(5, 8), range(8, 11), baseCost)
fill(missileJetAffinity, range(8, 11), range(11, 15), baseCost)
fill(missileJetAffinity, range(11, 13), range(15, 19), baseCost)

numPopulation = 500
numGenes = 6
numGenerations = 200
# This is supposed to be relatively high.
crossoverRate = .90
# This is supposed to be relatively low.
mutationRate = .50

# Defining the population size.
# The population will have n chromosomes where each chromosome has m genes.
populationSize = (numPopulation, numGenes)

#Creating the initial population.
population = []
for i in range(numPopulation):
    newChromosome = numpy.concatenate(
            (sample(range(0, numJets), 2),
            sample(range(0, numPilots), 2),
            # This implies we will always assign 2 missiles to a jet at the moment.
            sample(range(0, numMissiles), 2)))
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

print(best)
print(best_eval)