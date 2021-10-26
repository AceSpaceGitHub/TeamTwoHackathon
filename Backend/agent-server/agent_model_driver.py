import copy

from scenario_env import ScenarioEnv

def GeneratePrediction(model, scenarioEnv: ScenarioEnv):
    """
    Generates prediction from the agent model.
    """

    sampleEnvObs = scenarioEnv.reset()
    done = False
    score = 0
    prediction = []

    while not done:
        action, _ = model.predict(sampleEnvObs)
        sampleEnvObs, reward, done, _ = scenarioEnv.step(action)
        score+=reward
        recordedObs = copy.deepcopy(sampleEnvObs)
        print('Score:{} Action:{} State:{}'.format(score, action, [recordedObs["missles"], recordedObs["currentShipDamage"], recordedObs["assets"]]))
        prediction.append([action, [recordedObs["missles"], recordedObs["currentShipDamage"], recordedObs["assets"]]])
    scenarioEnv.close()

    return prediction
