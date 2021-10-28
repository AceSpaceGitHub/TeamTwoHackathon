import random
from random import randint, random, sample

from gene_constraints import *
from gene_utils import tournamentSelection

def computeFitness(chromosome, numSorties, sortieScheduleRequest):
    # We'll work to minimize mission length without
    # violating too many other constraints.
    chromoItr = iter(chromosome)
    tupledChromo = list(zip(chromoItr, chromoItr, chromoItr))
    sortedByMissionOffset = sorted(tupledChromo, key=lambda elem: elem[0])

    earliestSortieStart = sortedByMissionOffset[0][0]
    latestSortieEnd = earliestSortieStart
    sortieStarts = []
    sortieEnds = []
    for i in range(len(sortedByMissionOffset)):
        # Assuming any maintenance/downtime doesn't currently count, especially for last mission.
        # So at the moment this means we aren't deconflicting jets/pilots.
        sortieStart = sortedByMissionOffset[i][0]
        sortieStarts.append(sortieStart)

        sortieEnd = sortieStart + heloTimePadHours + sortieScheduleRequest[i] + heloTimePadHours
        sortieEnds.append(sortieEnd)

        latestSortieEnd = max(latestSortieEnd, sortieEnd)
    totalMissionLength = latestSortieEnd - earliestSortieStart

    # Check top-level mission constraints.
    cost = totalMissionLength
    if (totalMissionLength >= missionLengthHours):
        cost += 100

    # Check constraints across sortie level.

    # First off, are there any conflicting helo times?
    # This should use the pad constant more.
    # But actually it's only 1, so just check for uniqueness.
    #
    # Probably better if this ignored times that belonged to a different helo crew,
    # since this is implying multiple helo crews cannot be deployed at the same time.
    if (2 * numSorties) == len(set(sortieStarts + sortieEnds)):
        # Making this a hard constraint assuming one helo crew can't
        # support many sorties/be in two different places at the same hour/time.
        cost -= 1000

    return cost

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
                msnTimeOffset = i * genesPerSortie
                kid1[msnTimeOffset] = parent2[msnTimeOffset]
                kid2[msnTimeOffset] = parent1[msnTimeOffset]
        elif 33 < crossoverType and crossoverType < 66:
            for i in range(numSorties):
                strikeOffset = i * genesPerSortie + 1
                kid1[strikeOffset] = parent2[strikeOffset]
                kid2[strikeOffset] = parent1[strikeOffset]
        elif 66 < crossoverType and crossoverType < 100:
            for i in range(numSorties):
                heloOffset = i * genesPerSortie + 2
                kid1[heloOffset] = parent2[heloOffset]
                kid2[heloOffset] = parent1[heloOffset]
    return [kid1, kid2]

def mutation(chromosome, mutationRate, genesPerSortie, numSorties, remainingMissionTimeHours):
    for i in range(len(chromosome)):
        if random() < mutationRate:
            sortieOffset = i % genesPerSortie
            if (sortieOffset == 0):
                # Again, kludge? We don't want to lose sorties
                # starting towards the start of the mission offset.
                # Freely scramble the other mission offsets though.
                if (chromosome[i] != 0):
                    chromosome[i] = randint(0, remainingMissionTimeHours - 1 // 4)
            elif (sortieOffset == 1):
                # We can't really repeat tasks.
                # Choose a random buddy to swap with for now,
                # maybe we should just create a super penalty for this.
                sortieTask = chromosome[i]
                otherSortieTaskIdx = randint(0, numSorties-1) * genesPerSortie + 1
                otherSortieTask = chromosome[otherSortieTaskIdx]
                chromosome[i] = otherSortieTask
                chromosome[otherSortieTaskIdx] = sortieTask
            elif (sortieOffset == 2):
                # Well. There's only two helos at the moment.
                # So randint may not even mutate things. So flip it.
                flippedHelo = None
                if (chromosome[i] == 1):
                    flippedHelo = 0
                else:
                    flippedHelo = 1
                chromosome[i] = flippedHelo

# If we wanted to be super cool, this could maybe be generic and take
# in the unique crossover/generate initial population/etc functions.
# Would need to look up the Pythonic way of doing this. The footprint
# of a simple genetic algo like this isn't large anyway.
# 
# Also, at the moment other than # sorties,
# this is mostly going to obey the constraints
# spelled out elsewhere as constants.
def scheduleStrikePackages(numGenerations, numPopulation,
    remainingMissionTimeHours, sortieScheduleRequest,
    crossoverRate=.99, mutationRate=.10):
    # 1 mission time offset, 1 strike package, 1 assigned helo crew.
    genesPerSortie = 3
    numSorties = len(sortieScheduleRequest)

    # Creating the initial population.
    population = []
    for i in range(numPopulation):
        newChromosome = []
        for i in range(numSorties):
            newChromosome += sample(range(0, remainingMissionTimeHours), 1)
            newChromosome += [i]
            newChromosome += sample(range(0, numHeloCrews), 1)
        
        # Kludge? Something's gotta go first. But right now
        # the algo will just procrastinate and push everything to some arbitrary
        # time(s) before the end of the mission window, so force its hand a little.
        newChromosome[randint(0, numSorties - 1) * genesPerSortie] = 0

        population.append(newChromosome)

    best, best_eval = 0, computeFitness(population[0], numSorties, sortieScheduleRequest)
    for genIdx in range(numGenerations):
        # Compute fitness of all candidate chromosomes.
        scores = [computeFitness(c, numSorties, sortieScheduleRequest) for c in population]

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
                mutation(child, mutationRate, genesPerSortie, numSorties, remainingMissionTimeHours)
                children.append(child)
        population = children
    return best

scheduleStrikePackages(50, 100, 724, {
    0: 6,
    1: 6,
    2: 4,
    3: 3,
    4: 4,
    5: 5,
})