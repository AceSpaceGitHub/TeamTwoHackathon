import random
from random import randint, random, sample

from gene_constraints import *
from gene_utils import tournamentSelection

def computeFitness(chromosome, numSorties, genesPerSortie, sortieToMissileRequest):
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

        sortieMissileCapacities = sorted([jetMissileCapacity[jetIdx1], jetMissileCapacity[jetIdx2]])
        requestedMissileLoadout = sorted(sortieToMissileRequest[chromosome[offsetIdx + 4]])
        canJetsAccommodateRequest = len(sortieMissileCapacities) == len(requestedMissileLoadout)
        if (canJetsAccommodateRequest):
            for i in range(len(sortieMissileCapacities)):
                canJetsAccommodateRequest &= sortieMissileCapacities[i] >= requestedMissileLoadout[i]
        if canJetsAccommodateRequest:
            avgSortieScore += -100
        else:
            avgSortieScore += 1000

        # This is the score we want to minimize across sorties.
        # Cost generally will roughly equate to if strike package entities are
        # compatible or are otherwise collocated (so smaller time or distance cost).
        avgSortieScore += (jetToJetScore + pilotToPilotScore + pilotToJetScore)

    # Don't just spam the same jets/pilots over and over.
    allJetIndices = []
    allPilotIndices = []
    for i in range(numSorties):
        sortieStartIdx = i * genesPerSortie
        allJetIndices.append(chromosome[sortieStartIdx])
        allJetIndices.append(chromosome[sortieStartIdx + 1])
        allPilotIndices.append(chromosome[sortieStartIdx + 2])
        allPilotIndices.append(chromosome[sortieStartIdx + 3])

    if len(allJetIndices) == len(set(allJetIndices)):
        avgSortieScore -= 100
    else:
        avgSortieScore += 500

    if len(allPilotIndices) == len(set(allPilotIndices)):
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

def crossover(parent1, parent2, crossoverRate, genesPerSortie, numSorties):
    # Create two kids from two parents.
    kid1, kid2 = parent1.copy(), parent2.copy()
    # We wanna crossover parts of what made the parents
    # good but should we also risk creating invalid schedules (e.g. repeated tasks)?
    # Let's just randomly choose an attribute to switch for now.
    if random() < crossoverRate:
        crossoverType = random()  * 100
        if 0 < crossoverType and crossoverType < 33:
            for i in range(numSorties):
                jetOffset = i * genesPerSortie
                nextJetOffset = jetOffset + 1
                kid1[jetOffset] = parent2[jetOffset]
                kid1[nextJetOffset] = parent2[nextJetOffset]
                kid2[jetOffset] = parent1[jetOffset]
                kid2[nextJetOffset] = parent1[nextJetOffset]
        elif 33 < crossoverType and crossoverType < 66:
            for i in range(numSorties):
                pilotOffset = i * genesPerSortie + 2
                nextPilotOffset = pilotOffset + 1
                kid1[pilotOffset] = parent2[pilotOffset]
                kid1[nextPilotOffset] = parent2[nextPilotOffset]
                kid2[pilotOffset] = parent1[pilotOffset]
                kid2[nextPilotOffset] = parent1[nextPilotOffset]
        elif 66 < crossoverType and crossoverType < 100:
            for i in range(numSorties):
                taskOffset = i * genesPerSortie + 4
                kid1[taskOffset] = parent2[taskOffset]
                kid2[taskOffset] = parent1[taskOffset]
    return [kid1, kid2]

def mutation(chromosome, mutationRate, genesPerSortie, numSorties):
    for i in range(len(chromosome)):
        if random() < mutationRate:
            sortieOffset = i % genesPerSortie
            # Flip the resource index to another random valid index.
            if (sortieOffset == 0) or (sortieOffset == 1):
                chromosome[i] = randint(0, numJets-1)
            elif (sortieOffset == 2) or (sortieOffset == 3):
                chromosome[i] = randint(0, numPilots-1)
            elif (sortieOffset == 4):
                # Except for tasks. We can't really repeat those.
                # Choose a random buddy to swap with for now,
                # maybe we should just create a super penalty for this.
                sortieTask = chromosome[i]
                otherSortieTaskIdx = randint(0, numSorties-1) * genesPerSortie + 4
                otherSortieTask = chromosome[otherSortieTaskIdx]
                chromosome[i] = otherSortieTask
                chromosome[otherSortieTaskIdx] = sortieTask

# If we wanted to be super cool, this could maybe be generic and take
# in the unique crossover/generate initial population/etc functions.
# Would need to look up the Pythonic way of doing this. The footprint
# of a simple genetic algo like this isn't large anyway.
# 
# Also, at the moment other than # sorties,
# this is mostly going to obey the constraints
# spelled out elsewhere as constants.
def allocateStrikePackages(numGenerations, numPopulation,
    sortieToMissileRequest, crossoverRate=.99, mutationRate=.10):
    # 2 jets, 2 pilots, 1 task that maps to a missle loadout request.
    genesPerSortie = 5
    numSorties = len(sortieToMissileRequest)

    # Creating the initial population.
    population = []
    for i in range(numPopulation):
        newChromosome = []
        for i in range(numSorties):
            newChromosome += sample(range(0, numJets), 2)
            newChromosome += sample(range(0, numPilots), 2)
            newChromosome += [i]
        population.append(newChromosome)

    best, best_eval = 0, computeFitness(population[0], numSorties, genesPerSortie, sortieToMissileRequest)
    for genIdx in range(numGenerations):
        # Compute fitness of all candidate chromosomes.
        scores = [computeFitness(c, numSorties, genesPerSortie, sortieToMissileRequest) for c in population]

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
            for child in crossover(parent1, parent2, crossoverRate, genesPerSortie, numSorties):
                mutation(child, mutationRate, genesPerSortie, numSorties)
                children.append(child)
        population = children
    return best
