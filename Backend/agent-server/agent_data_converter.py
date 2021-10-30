import datetime
from stable_baselines3.common.env_checker import check_env

from gene_constraints import *

def GetScenarioEnvironmentInputs(operatingContext):
    """
    Converts operating context (aka JSON dictionary) from client
    to scenario environment agent can understand.
    """

    numJets = operatingContext['numJets']
    numPilots = operatingContext['numPilots']
    numMissiles = operatingContext['numMissiles']

    desiredDamages = []
    for entry in operatingContext['intendedTargetIdToDamage']['entries']:
        desiredDamages.append(entry['damage'])

    return numJets, numPilots, numMissiles, desiredDamages

def GeneratePlanAssessment(prediction, targetIds):
    """
    Converts prediction results to plan assessment client expects.
    """
    sortieActions = []
    numJets = 0
    numPilots = 0
    numMissiles = 0

    results = prediction['Results']
    for result in results:
        # Translate the per-sortie action data.
        for action in result['Actions']:
            actionTaken = action['Actions']
            actionMidIdx = len(actionTaken) // 2

            targettedIds = []
            for i in range(0, actionMidIdx):
                targettedIds.append(targetIds[actionTaken[i]])

            missileLoadouts = []
            for i in range(actionMidIdx, len(actionTaken)):
                missileLoadouts.append(str(actionTaken[i]))

            sortieActions.append({
                'targetIds': targettedIds,
                'missileLoadouts': missileLoadouts
            })

            assets = action['Assets']
            numPilots = assets[0]
            numJets = assets[1]

            numMissiles = action['Missiles']

        # Translate the per-target state data.
        targetStateEntries = []
        targetRates = result['TargetRates']
        for targetRateIdx in range(len(targetRates)):
            targetStateEntries.append({
                'id': targetIds[targetRateIdx],
                'chanceOfSuccess': targetRates[targetRateIdx]
            })

    return {
        'sortieActions': sortieActions,
        'resultingState': {
            'vehiclesRemaining': numJets,
            'peopleRemaining': numPilots,
            'missilesRemaining': numMissiles,
            'targetState': { 'entries': targetStateEntries }
        }
    }

def GenerateSortieMissileRequest(planAssessment):
    sortieMissileRequest = {}
    sortieActions = planAssessment['sortieActions']
    for i in range(len(sortieActions)):
        sortieMissileRequest[i] = []
        missileLoadouts = sortieActions[i]['missileLoadouts']
        for j in range(len(missileLoadouts)):
            sortieMissileRequest[i].append(int(missileLoadouts[j]))
    return sortieMissileRequest

def GenerateScheduleRequest(planAssessment):
    sortieToTargetIds = {}
    sortieToLengthHours = {}
    sortieActions = planAssessment['sortieActions']
    for i in range(len(sortieActions)):
        targetIds = sortieActions[i]['targetIds']
        targetSortieTimes = []
        for j in range(len(targetIds)):
            targetSortieTimes.append(targetIdToSortieTimeHours[targetIds[j]])
        sortieToTargetIds[i] = targetIds
        sortieToLengthHours[i] = max(targetSortieTimes)
    return sortieToTargetIds, sortieToLengthHours

def CreateHeloAction(strikePackage, actionStartTimestamp):
    # Form the helo action.
    # At the moment, intelligent helo assignment isn't done
    # based off what/where the strike package is,
    # so just take the helos from the same carrier as one of the jets.
    jetIdx1 = strikePackage[0]
    carrierId = None
    heloIds = None
    heloCrewIds = None
    if isJetOnCarrier[0][jetIdx1] == 1:
        carrierId = "Carrier A"
        heloIds = ["Helo 1", "Helo 2"]
        heloCrewIds = ["Helo Crew 1", "Helo Crew 2"]
    elif isJetOnCarrier[1][jetIdx1] == 1:
        carrierId = "Carrier B"
        heloIds = ["Helo 3", "Helo 4"]
        heloCrewIds = ["Helo Crew 3", "Helo Crew 4"]

    return {
        "type": 0,
        "targetList": [],
        "involvedVehicles": heloIds,
        "departingCarrier": carrierId,
        "involvedPersonelle": heloCrewIds,
        "numberOfMissiles": [],
        "startTime": actionStartTimestamp.strftime("%H:%M:%S"),
        "endTime": (actionStartTimestamp + datetime.timedelta(hours=heloTimePadHours)).strftime("%H:%M:%S")
    }

def CreateStrikeAction(strikePackage, strikeLoadout, strikeTargetIds,
    strikeLengthHours, actionStartTimestamp):
    # At the moment we're assuming all jets/pilots present,
    # so there's not a real index -> actual id/name lookup here.
    jetIdx1 = strikePackage[0]
    jetId1 = "Jet " + str(strikePackage[0] + 1)
    jetId2 = "Jet " + str(strikePackage[1] + 1)
    pilotId1 = "Pilot " + str(strikePackage[2] + 1)
    pilotId2 = "Pilot " + str(strikePackage[3] + 1)

    carrierId = None
    if isJetOnCarrier[0][jetIdx1] == 1:
        carrierId = "Carrier A"
    elif isJetOnCarrier[1][jetIdx1] == 1:
        carrierId = "Carrier B"

    return {
        "type": 1,
        "targetList": strikeTargetIds,
        "involvedVehicles": [jetId1, jetId2],
        "departingCarrier": carrierId,
        "involvedPersonelle": [pilotId1, pilotId2],
        "numberOfMissiles": strikeLoadout,
        "startTime": actionStartTimestamp.strftime("%H:%M:%S"),
        "endTime": (actionStartTimestamp + datetime.timedelta(hours=strikeLengthHours)).strftime("%H:%M:%S")
    }

def AssembleSortieData(planAssessment, strikePackages, strikeSchedule,
    strikesToTargetIds, strikeToLengthHours, strikeLoadouts):
    strikePackageItr = iter(strikePackages)
    strikePackageTuples = sorted(list(zip(strikePackageItr, strikePackageItr, strikePackageItr,
        strikePackageItr, strikePackageItr)), key=lambda elem: elem[4])
    strikeScheduleItr = iter(strikeSchedule)
    strikeScheduleTuples = sorted(list(zip(strikeScheduleItr, strikeScheduleItr, strikeScheduleItr)),
        key=lambda elem: elem[1])

    numStrikePackages = len(strikePackageTuples)
    strikeActions = planAssessment['sortieActions']
    if (numStrikePackages != len(strikeActions)):
        raise 'Strike action and package sizes do not match.'
    if (numStrikePackages != len(strikeScheduleTuples)):
        raise 'Strike package and schedule sizes do not match.'

    resultingActions = []
    for i in range(numStrikePackages):
        strikePackage = strikePackageTuples[i]
        strikeSchedule = strikeScheduleTuples[i]

        sortieStartTime = (datetime.datetime.strptime(missionStartTime, '%H:%M:%S')
            + datetime.timedelta(hours=strikeToLengthHours[i]))
        firstHeloAction = CreateHeloAction(strikePackage, sortieStartTime)
        resultingActions.append(firstHeloAction)

        sortieStartTime = (datetime.datetime.strptime(firstHeloAction['endTime'], '%H:%M:%S'))
        strikeAction = CreateStrikeAction(strikePackage, strikeLoadouts[i],
            strikesToTargetIds[i], strikeToLengthHours[i], sortieStartTime)
        resultingActions.append(strikeAction)

        sortieStartTime = (datetime.datetime.strptime(strikeAction['endTime'], '%H:%M:%S'))
        secondHeloAction = CreateHeloAction(strikePackage, sortieStartTime)
        resultingActions.append(secondHeloAction)

    return resultingActions