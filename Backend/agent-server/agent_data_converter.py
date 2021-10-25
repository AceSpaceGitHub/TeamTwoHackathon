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
    Converts agent observation space to prediction results client expects.
    """
    return []