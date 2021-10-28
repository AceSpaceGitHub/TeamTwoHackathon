from stable_baselines3.common.env_checker import check_env

from scenario_env import ScenarioEnv

def OperatingContextToScenarioEnvironment(operatingContext):
    """
    Converts operating context (aka JSON dictionary) from client
    to scenario environment agent can understand.
    """

    # We anticipate using num jets/pilots, just the scenario
    # doesn't officially take them in yet.
    numJets = 0
    numPilots = 0
    numMissiles = 0
    for carrier in operatingContext['friendlyForces']['carriers']:
        for squadron in carrier['squadrons']:
            numJets += len(squadron['jetIds'])
            numPilots += len(squadron['pilotIds'])
            numMissiles += len(squadron['missileIds'])

    desiredDamages = []
    for entry in operatingContext['intendedTargetIdToDamage']['entries']:
        desiredDamages.append(entry['damage'])
    
    scenarioEnv = ScenarioEnv(numMissiles,
        desiredDamages[0], desiredDamages[1], desiredDamages[2],
        desiredDamages[3], desiredDamages[4], desiredDamages[5])
    check_env(scenarioEnv, warn=True)

    return scenarioEnv

def PredictionToPlanAssessment(prediction, targetIds):
    """
    Converts prediction results to plan assessment client expects.
    """
    sortieActions = []
    resultingStates = []
    for step in prediction:
        actionTaken = step[0]
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

        stateContents = step[1]
        numMissiles = stateContents[0]

        targetIdToDamage = {}
        targetIdxToDamage = stateContents[1]
        for targetIdx in range(0, len(targetIdxToDamage)):
            targetIdToDamage[targetIds[targetIdx]] = str(targetIdxToDamage[targetIdx])

        numJets = stateContents[2][0]
        numPilots = stateContents[2][1]

        resultingStates.append({
            'numMissiles': str(numMissiles),
            'numJets': str(numJets),
            'numPilots': str(numPilots),
            'targetIdToDamage': targetIdToDamage
        })

    return {
        'sortieActions': sortieActions,
        'resultingStates': resultingStates
    }

def PlanAssessmentToSortieMissileRequest(planAssessment):
    sortieMissileRequest = {}
    sortieActions = planAssessment['sortieActions']
    for i in range(len(sortieActions)):
        sortieMissileRequest[i] = []
        missileLoadouts = sortieActions[i]['missileLoadouts']
        for j in range(len(missileLoadouts)):
            sortieMissileRequest[i].append(int(missileLoadouts[j]))
    return sortieMissileRequest