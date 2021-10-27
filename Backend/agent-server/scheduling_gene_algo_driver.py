import random
from random import randint, random, sample, shuffle

from gene_constraints import *
from gene_utils import tournamentSelection

def inSameCarrier(heloIdx, sortieIdx):
    return (heloToCarrier[heloIdx], sortieToCarrier[sortieIdx])

def computeFitness(chromosome):
    # Work to minimize mission length without
    # violating too many other constraints.
    chromoItr = iter(chromosome)
    tupledChromo = list(zip(chromoItr, chromoItr, chromoItr))
    sortedByMissionOffset = sorted(tupledChromo, key=lambda elem: elem[0])

    # Assuming any maintenance/downtime doesn't count for last mission.
    # If that's not true can just add those missing times.
    latestSortieStart = sortedByMissionOffset[numSorties-1][0] + sortieTimeHours + heloTimePadHours
    earliestSortieStart = sortedByMissionOffset[0][0]
    totalMissionLength = latestSortieStart - earliestSortieStart

    # Check top-level mission constraints.
    cost = totalMissionLength
    if (totalMissionLength >= missionLengthHours):
        cost += 100
    if (earliestSortieStart < missionLengthHours // 4):
        cost -= 25

    # Check basic constraints per sortie level.
    for i in range(len(sortedByMissionOffset)):
        if (inSameCarrier(sortedByMissionOffset[i][1], sortedByMissionOffset[i][2])):
            cost -= 10

    # Check constraints across sortie level.
    # Should probably take maintenance/downtime into account?
    # At this level we don't know what's in the sortie necessarily.
    singleSortieLengthHours = heloTimePadHours + sortieTimeHours + heloTimePadHours
    sortieStartTimesHours = [x[0] for x in sortedByMissionOffset]
    sortieEndTimeHours = [x[0] + singleSortieLengthHours for x in sortedByMissionOffset]

    # Are there conflicting helo times?
    # This should use the pad constant.
    # But actually it's only 1, so just check for uniqueness.
    # Probably better if this ignored times that belonged to a different helo crew.
    if (2 * numSorties) == len(set(sortieStartTimesHours + sortieEndTimeHours)):
        # Making this a hard constraint assuming one helo crew can't
        # support many sorties/be in two different places at the same hour/time.
        cost -= 100

    return cost

def crossover(parent1, parent2, crossoverRate):
    # Create two kids from two parents.
    kid1, kid2 = parent1.copy(), parent2.copy()
    # Check for recombination chance.
    if random() < crossoverRate:
        # We wanna crossover parts of what made the parents
        # good but should we also risk creating invalid schedules (e.g. repeated tasks)?
        # Let's just randomly choose an attribute to switch for now.
        crossoverType = random()  * 100
        if 0 < crossoverType and crossoverType < 33:
            for i in range(numSorties):
                msnOffsetIdx = 3 * i
                kid1[msnOffsetIdx] = parent2[msnOffsetIdx]
                kid2[msnOffsetIdx] = parent1[msnOffsetIdx]
        elif 33 < crossoverType and crossoverType < 66:
            for i in range(numSorties):
                heloIdx = 3 * i + 1
                kid1[heloIdx] = parent2[heloIdx]
                kid2[heloIdx] = parent1[heloIdx]
        else:
            for i in range(numSorties):
                taskIdx = 3 * i + 2
                kid1[taskIdx] = parent2[taskIdx]
                kid2[taskIdx] = parent1[taskIdx]
    return [kid1, kid2]

def mutation(chromosome, mutationRate):
    for i in range(len(chromosome)):
        if random() < mutationRate:
            idxMod = i % 3
            if idxMod == 0:
                chromosome[i] = randint(0, missionLengthHours)
            elif idxMod == 1:
                # Well. There's only two helos at the moment.
                # So randint may not even mutate things.
                flippedHelo = None
                if (bool(chromosome[i])):
                    flippedHelo = 0
                else:
                    flippedHelo = 1
                chromosome[i] = flippedHelo
            # Gets tricky mutating the sortie since we can't
            # repeat them in this context. Let's leave that alone for now.
            # We could just pick a random entry to swap with.

numPopulation = 1000
# 1 msn offset, 1 helo crew, 1 strike crew/task per sortie.
numGenes = numSorties * 3
numGenerations = 100
# This is supposed to be relatively high.
crossoverRate = .99
# This is supposed to be relatively low.
mutationRate = .12

# Defining the population size.
# The population will have n chromosomes where each chromosome has m genes.
populationSize = (numPopulation, numGenes)

# Creating the initial population.
population = []
for i in range(numPopulation):
    newChromosome = []
    sortieIndices = list(range(0, numSorties))
    shuffle(sortieIndices)
    for i in range(numSorties):
        newChromosome += sample(range(0, missionLengthHours), 1)
        newChromosome += sample(range(0, numHeloCrews), 1)
        newChromosome.append(sortieIndices[i])
    population.append(newChromosome)

best, best_eval = 0, computeFitness(population[0])
for genIdx in range(numGenerations):
    # Compute fitness of all candidate chromosomes.
    scores = [computeFitness(c) for c in population]

    # Check for new best.
    for i in range(numPopulation):
        if scores[i] < best_eval:
            best, best_eval = population[i], scores[i]
            print(">%d, new best f(%s) = %.3f" % (genIdx,  population[i], scores[i]))

    # Select parents.
    selected = [tournamentSelection(population, scores) for _ in range(numPopulation)]

    # Create the next generation from the parents.
    children = list()
    for i in range(0, numPopulation, 2):
        parent1, parent2 = selected[i], selected[i+1]
        for child in crossover(parent1, parent2, crossoverRate):
            mutation(child, mutationRate)
            children.append(child)
    population = children
