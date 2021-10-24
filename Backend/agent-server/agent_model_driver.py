import copy

from gym import Env
from gym.spaces import Discrete, Dict, MultiBinary, MultiDiscrete, Box
import numpy as np
import random
from stable_baselines3 import PPO

class ScenarioManager:
    def getActionSpace(self):
        return MultiDiscrete([6, 6, 2, 2])
    def getObservationSpace(self):
        return Dict({"missles": Discrete(100), 
        "expectedShipDamage": MultiDiscrete([3,3,3,3,3,3]), 
        "currentShipDamage": MultiDiscrete([3,3,3,3,3,3]), 
        "target1Defense": MultiDiscrete([100,100,100,100,100,100]),
        "target2Defense": MultiDiscrete([100,100,100,100,100,100]),
        "target3Defense": MultiDiscrete([100,100,100,100,100,100]),
        "target4Defense": MultiDiscrete([100,100,100,100,100,100]),
        "target5Defense": MultiDiscrete([100,100,100,100,100,100]),
        "target6Defense": MultiDiscrete([100,100,100,100,100,100]),
        "target1Targets": MultiBinary(6),
        "target2Targets": MultiBinary(6),
        "target3Targets": MultiBinary(6),
        "target4Targets": MultiBinary(6),
        "target5Targets": MultiBinary(6),
        "target6Targets": MultiBinary(6),
        "assets": MultiDiscrete([100,100])})
    def getState(self, numberOfMissles, tD1, tD2, tD3, tD4, tD5, tD6):
        return {"missles": numberOfMissles,
         "expectedShipDamage": np.array([tD1, tD2, tD3, tD4, tD5, tD6]), 
         "currentShipDamage": np.array([0,0,0,0,0,0]),
         "target1Defense": np.array([0,0,25,0,15,0]),
         "target2Defense": np.array([0,0,0,25,0,15]),
         "target3Defense": np.array([0,0,30,0,0,0]),
         "target4Defense": np.array([0,0,0,30,0,0]),
         "target5Defense": np.array([0,0,0,0,40,0]),
         "target6Defense": np.array([0,0,0,0,0,40]),
         "target1Targets": np.array([1, 0, 1, 0 , 0, 0]),
         "target2Targets": np.array([0, 1, 0, 1 , 0, 0]),
         "target3Targets": np.array([1, 0, 1, 0 , 0, 0]),
         "target4Targets": np.array([0, 1, 0, 1 , 0, 0]),
         "target5Targets": np.array([0, 0, 0, 0 , 1, 1]),
         "target6Targets": np.array([0, 0, 0, 0 , 1, 1]),
         "assets": np.array([50,50])}
    def canAttack(self, state, sortiArray, ship1, ship2):
        canAttack = False
        reward = -50
        # Check if can attack
        for sorti in sortiArray:
            if state[sorti][ship1] and state[sorti][ship2]:
                canAttack = True
                reward = 10
                break
        return canAttack, reward
    def shouldAttack(self, state, defenseArray, ship):
        reward = 0
        shouldAttack = True
        # Check if ship is already more damaged than expected
        if state["currentShipDamage"][ship] >= state["expectedShipDamage"][ship]:
            # Check to see if target posses a threat
            if(state["currentShipDamage"][ship] == 0 and state[defenseArray[ship]][ship] > 0):
                # Reward for damaging a ship that is a threat?
                reward = 0
            else:
                # no threat and already at expected damage
                reward = -50
                shouldAttack = False
        else:
            # targetted a ship worth targetting
            reward = 10
        return shouldAttack, reward
    def defendShip(self, state, defenseArray, ship):
        shotDown = False
        length = len(state[defenseArray[ship]])
        for index in range(0, length):
            if(state[defenseArray[ship]][index] > 0):
                roll = random.randint(0,100)
                if(roll <= state[defenseArray[ship]][index]):
                    shotDown = True
        return shotDown
    def shootShip(self, state, ship, defenseArray):
        reward = 0
        roll = random.randint(0, 100)
        if roll <= 60:
            # Should we reward more here?
            state["currentShipDamage"][ship] = max(1, state["currentShipDamage"][ship])
            for index in defenseArray:
                state[index][ship] = 0
        
            roll = random.randint(0, 100)
            if roll <= 50:
                # Should we reward more here?
                state["currentShipDamage"][ship] = max(2, state["currentShipDamage"][ship])
        
        return reward
    def step(self, state, action):
        # Set placeholder for info
        info = {}
        reward = 0
        done = False
        numberOfTargets = 6
        defenseArray = ["target1Defense", "target2Defense", "target3Defense", "target4Defense", "target5Defense", "target6Defense"]
        sortieArray = ["target1Targets", "target2Targets", "target3Targets", "target4Targets", "target5Targets", "target6Targets"]

        # Should we reward here or after hit or even after checking against expected damage?
        ship1Index = action[0]
        ship2Index = action[1]

        canAttack , canAttackReward = self.canAttack(state, sortieArray, ship1Index, ship2Index)

        if canAttack:
            shouldAttack, shouldAttackReward1 = self.shouldAttack(state, sortieArray, ship1Index)
            self.shootShip(state, ship1Index, defenseArray)
            state["missles"] -= 1
            self.shootShip(state, ship1Index, defenseArray)
            state["missles"] -= 1
            shouldAttack2, shouldAttackReward2 = self.shouldAttack(state, sortieArray, ship2Index)
            self.shootShip(state, ship2Index, defenseArray)
            state["missles"] -= 1
            self.shootShip(state, ship2Index, defenseArray)
            state["missles"] -= 1
            reward = canAttackReward + shouldAttackReward1 + shouldAttackReward2
        else:
            # Can't attack we are done
            return state, canAttackReward, False, info

        isExpectedDamageMet = True
        for shipIndex in range(0, numberOfTargets):
            if state["currentShipDamage"][shipIndex] < state["expectedShipDamage"][shipIndex]:
                isExpectedDamageMet = False
                break
        
        if isExpectedDamageMet:
            reward += 100
            done = True

        if state["missles"] <= 0:
            done = True

        if state["assets"][0] <= 0 or state["assets"][1] <= 0:
            done = True

        # Return step information
        return state, reward, done, info

class ScenarioEnv(Env):
    def __init__(self, numberOfMissles, tD1, tD2, tD3, tD4, tD5, tD6):
        manager = ScenarioManager()
        self.manager = manager
        # Actions we can take: 0 - Do Nothing, 1 - Launch
        self.action_space = manager.getActionSpace()
        # Target Damage state array: 0 - Untouched, 1 - Disabled, 2 - Destroyed
        self.observation_space = manager.getObservationSpace()
        # store initial state
        self.numberOfMissles = numberOfMissles
        self.tD1 = tD1
        self.tD2 = tD2
        self.tD3 = tD3
        self.tD4 = tD4
        self.tD5 = tD5
        self.tD6 = tD6
        # Set start state
        self.state = self.manager.getState(self.numberOfMissles, self.tD1, self.tD2, self.tD3, self.tD4, self.tD5, self.tD6)

    def step(self, action):
        # Return step information
        return self.manager.step(self.state, action)

    def render(self):
        # Implement viz
        pass

    def reset(self):
        # Reset shower temperature
        self.state = self.manager.getState(self.numberOfMissles, self.tD1, self.tD2, self.tD3, self.tD4, self.tD5, self.tD6)
        return self.state

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
