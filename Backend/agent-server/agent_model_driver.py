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
        print('Score:{} Action:{} State:{}'.format(score, action, [sampleEnvObs["missles"], sampleEnvObs["currentShipDamage"], sampleEnvObs["assets"]]))
        prediction.append([action, [sampleEnvObs["missles"], sampleEnvObs["currentShipDamage"], sampleEnvObs["assets"]]])
    scenarioEnv.close()

    return prediction
