import datetime
from gene_utils import fill, reflectedFill

# This all defines scenario data we can mess around
# with building into the algorithms. Of course ideally this
# would be generated on the fly per request/scenario.

missionStartTime = "08:00:00"

numCarriers = 2
numJets = 19
numHeloCrews = 2
numPilots = 21

minJetsPerSortie = 2
maxMissilesPerJet = 2
missionLengthHours = 7 * 24
heloTimePadHours = 1

# Create affinity matrices.
#
# So actually since we want to minimize our fitness cost,
# this is actually sort of reverse notion of affinity
# (lower score, more compatible). Should probably just
# flip to maximizing costs so that's less confusing.
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

jetMissileCapacity = [maxMissilesPerJet] * numJets
jetMissileCapacity[3] = jetMissileCapacity[7] = jetMissileCapacity[8] = jetMissileCapacity[16] = 1

isJetOnCarrier = [[0] * numJets for i in range(numCarriers)]
fill(isJetOnCarrier, range(0, 1), range(0, 11), 1)
fill(isJetOnCarrier, range(1, 2), range(11, 19), 1)

targetIdToSortieTimeHours = {
    "Enemy Carrier A": 4,
    "Enemy Carrier B": 5,
    "Enemy Destroyer A": 4,
    "Enemy Destroyer B": 5,
    "Enemy Cruiser A": 6,
    "Enemy Cruiser B": 6,
}
