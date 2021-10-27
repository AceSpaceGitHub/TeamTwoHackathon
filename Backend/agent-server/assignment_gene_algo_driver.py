import random
from random import randint, random, sample

from gene_constraints import *
from gene_utils import tournamentSelection

# 2 jets, 2 pilots, max 4 missiles.
# Well, let's assume 4 missiles always for now. 
# We could make it interesting and let it assign <2 missiles
# and reward/penalize accordingly.
genesPerSortie = 8
chromosomeWidth = genesPerSortie * numSorties

def inSameCarrier(jetIdx1, jetIdx2, pilotIdx1, pilotIdx2):
    return (jetToCarrier[0][jetIdx1] == jetToCarrier[0][jetIdx2]
    == pilotToCarrier[0][pilotIdx1] == pilotToCarrier[0][pilotIdx2])

def inSameSquadron(jetIdx1, jetIdx2, pilotIdx1, pilotIdx2):
    return (jetToSquadron[0][jetIdx1] == jetToSquadron[0][jetIdx2]
    == pilotToSquadron[0][pilotIdx1] == pilotToSquadron[0][pilotIdx2])

def computeFitness(chromosome):
    avgSortieScore = 0
    for i in range(numSorties):
        offsetIdx = genesPerSortie*i
        jetIdx1 = chromosome[offsetIdx + 0]
        jetIdx2 = chromosome[offsetIdx + 1]
        jetToJetScore = jetAffinity[jetIdx1][jetIdx2]
        pilotIdx1 = chromosome[offsetIdx + 2]
        pilotIdx2 = chromosome[offsetIdx + 3]
        pilotToPilotScore = pilotAffinity[pilotIdx1][pilotIdx2]
        pilotToJetScore = pilotJetAffinity[pilotIdx1][jetIdx1] + pilotJetAffinity[pilotIdx2][jetIdx2]

        # This is the score we want to minimize across sorties.
        # Cost generally will roughly equate to if strike package entities are
        # compatible or are otherwise collocated (so smaller time or distance cost).
        avgSortieScore += (jetToJetScore + pilotToPilotScore + pilotToJetScore)

    # Don't spam the same jets/pilots over and over.
    allJetIndices = []
    allPilotIndices = []
    for i in range(numSorties):
        sortieStartIdx = i * genesPerSortie
        allJetIndices.append(chromosome[sortieStartIdx])
        allJetIndices.append(chromosome[sortieStartIdx + 1])
        allPilotIndices.append(chromosome[sortieStartIdx + 2])
        allPilotIndices.append(chromosome[sortieStartIdx + 3])

    if numSorties * 2 == len(set(allJetIndices)):
        avgSortieScore -= 100
    else:
        avgSortieScore += 500

    if numSorties * 2 == len(set(allPilotIndices)):
        avgSortieScore -= 100
    else:
        avgSortieScore += 500

    return avgSortieScore / numSorties

def tournamentSelection(population, scores, k = 25):
    # Pit individuals against each other in a tournament and select the best.
    tournamentSize = min(k, len(population))
    selectionIdx = randint(0, len(population)-1)
    for i in range(0, tournamentSize-1):
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
        halfWidth = chromosomeWidth // 2
        kid1 = parent1[:halfWidth] + parent2[halfWidth:]
        kid2 = parent2[:halfWidth] + parent1[halfWidth:]
    return [kid1, kid2]

def mutation(chromosome, mutationRate):
    for i in range(len(chromosome)):
        if random() < mutationRate:
            sortieOffset = i % genesPerSortie
            # Flip the resource index to another random valid index.
            if (sortieOffset == 0) or (sortieOffset == 1):
                chromosome[i] = randint(0, numJets-1)
            elif (sortieOffset == 2) or (sortieOffset == 3):
                chromosome[i] = randint(0, numPilots-1)
            elif ((sortieOffset == 4) or (sortieOffset == 5)
                or (sortieOffset == 6) or (sortieOffset == 7)):
                chromosome[i] = randint(0, numMissiles-1)

# If we wanted to be super cool, this could maybe be generic and take
# in the unique crossover/generate initial population/etc functions.
# Would need to look up the Pythonic way of doing this. The footprint
# of a simple genetic algo like this isn't large anyway.
# 
# Also, at the moment this is mostly going to obey the constraints
# spelled out elsewhere as constants.
def allocateStrikePackages(numGenerations, numPopulation, crossoverRate, mutationRate):
    # Creating the initial population.
    population = []
    for i in range(numPopulation):
        newChromosome = []
        for i in range(numSorties):
            newChromosome += sample(range(0, numJets), 2)
            newChromosome += sample(range(0, numPilots), 2)
            newChromosome += sample(range(0, numPilots), 4)
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
    return best

allocateStrikePackages(50, 1000, .99, .12)