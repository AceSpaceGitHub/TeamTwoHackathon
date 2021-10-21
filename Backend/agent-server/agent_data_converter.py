from stable_baselines3.common.env_checker import check_env

from scenario_env import ScenarioEnv

def OperatingPictureToScenarioEnvironment(operatingPicture):
    """
    Converts operating context from client to scenario environment agent can understand.
    """
    numMissiles = operatingPicture.numMissiles

    desiredDamages = []
    for entry in operatingPicture.targetIdToDamage.entries:
        desiredDamages.append(entry.damage)
    
    scenarioEnv = ScenarioEnv(numMissiles,
        desiredDamages[0], desiredDamages[1], desiredDamages[2],
        desiredDamages[3], desiredDamages[4], desiredDamages[5])
    check_env(scenarioEnv, warn=True)

    return scenarioEnv

def PredictionToPlanAssessment(prediction, targetIds):
    """
    Converts agent observation space to prediction results client expects.
    """
    maxTargetIdx = (len(targetIds))
    actionAssessments = []
    for step in prediction:
        # Data in the action "column" is 1-based,
        # normalize to 0-based to access the intended ID.
        targetIdx = step[0] - 1
        actionTargetId = targetIds[targetIdx]
        numMissilesLeft = step[1][0]

        desiredDamages = step[1][1:maxTargetIdx+1]
        desiredDamageEntries = []
        for index, item in enumerate(desiredDamages):
            desiredDamageEntries.append(
                agent_pb2.TargetIdToDamageEntry(id=targetIds[index], damage=item))

        currentDamages = step[1][maxTargetIdx + 1:2*maxTargetIdx+1]
        currentDamageEntries = []
        for index, item in enumerate(currentDamages):
            currentDamageEntries.append(
                agent_pb2.TargetIdToDamageEntry(id=targetIds[index], damage=item))

        actionAssessment = agent_pb2.ActionAssessment(
            actionTargetId=actionTargetId, numMissilesLeft=numMissilesLeft,
            targetIdToCurrentDamage=agent_pb2.TargetToDamageMap(entries=currentDamageEntries),
            targetIdToDesiredDamage=agent_pb2.TargetToDamageMap(entries=desiredDamageEntries))
        actionAssessments.append(actionAssessment)

    return agent_pb2.PlanAssessment(actionAssessments=actionAssessments)