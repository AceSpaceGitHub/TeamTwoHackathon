
from stable_baselines3 import PPO
import gym
from gym import Env
from gym.spaces import Discrete, Dict, MultiBinary, MultiDiscrete
import numpy as np
import random

class DeterministicScenario:
    def getActionSpace(self):
        return MultiDiscrete([6, 6, 2, 2])
    def getObservationSpace(self):
        return Dict({"missiles": Discrete(100), 
        "expectedShipDamage": MultiDiscrete([100,100,100,100,100,100]), 
        "currentShipDamage": MultiDiscrete([100,100,100,100,100,100]), 
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
    def getRandomizedState(self):
        return {"missiles": random.randint(1, 99),
         "expectedShipDamage": 
         np.array([random.randint(0, 4), 
         random.randint(0, 4), 
         random.randint(0, 4), 
         random.randint(0, 4), 
         random.randint(0, 4), 
         random.randint(0, 4)]), 
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
         "assets": np.array([random.randint(1, 99), random.randint(1, 99)])}
    def getState(self, numberOfmissiles, numberOfJets, numberOfPilots, tD1, tD2, tD3, tD4, tD5, tD6):
        return {"missiles": numberOfmissiles,
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
         "assets": np.array([numberOfJets ,numberOfPilots])}
    def canAttack(self, state, sortiArray, ship1, ship2):
        canAttack = False
        reward = -10
        # Check if can attack
        for sorti in sortiArray:
            if state[sorti][ship1] and state[sorti][ship2]:
                canAttack = True
                reward = 20
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
                reward = -20
                shouldAttack = False
        else:
            # targetted a ship worth targetting
            reward = 100
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
    def shootShip(self, state, defenseArray, ship):
        reward = 0

        state["currentShipDamage"][ship] += 1

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

        if action[2] == 1:
            reward += 10
        if action[3] == 1:
            reward += 10

        canAttack , canAttackReward = self.canAttack(state, sortieArray, ship1Index, ship2Index)
        reward += canAttackReward
        if canAttack:

            shotDown1 = self.defendShip(state, defenseArray, ship1Index)
            shotDown2 = self.defendShip(state, defenseArray, ship2Index)

            if ship1Index == ship2Index:
                if shotDown1:
                    state["assets"][0] -= 1
                    state["assets"][1] -= 1
            else:
                if shotDown1:
                    state["assets"][0] -= 1
                    state["assets"][1] -= 1
                if shotDown2:
                    state["assets"][0] -= 1
                    state["assets"][1] -= 1

            shouldAttack, shouldAttackReward = self.shouldAttack(state, defenseArray, ship1Index)
            reward += shouldAttackReward
            self.shootShip(state, defenseArray, ship1Index)
            state["missiles"] -= 1
            if action[2] == 1:
                shouldAttack, shouldAttackReward = self.shouldAttack(state, defenseArray, ship1Index)
                reward += shouldAttackReward
                self.shootShip(state, defenseArray, ship1Index)
                state["missiles"] -= 1
            shouldAttack, shouldAttackReward = self.shouldAttack(state, defenseArray, ship2Index)
            reward += shouldAttackReward
            self.shootShip(state, defenseArray, ship2Index)
            state["missiles"] -= 1
            if action[3] == 1:
                shouldAttack, shouldAttackReward = self.shouldAttack(state, defenseArray, ship2Index)
                reward += shouldAttackReward
                self.shootShip(state, defenseArray, ship2Index)
                state["missiles"] -= 1
        else:
            # Can't attack we are done
            return state, canAttackReward, False, info
        
        # ############# Ideas #################
        # Count up assets instead of down. Add a cap and remove end condition for assets
        # Change Reward/Loss system for expected damage.
        #   Expected damage is now Expected hits. Remove Rolls
        # Add a calculated ratio reward for threats in the defending arrays
        # Add in standard deviation for rewards to encourage spreading out more hits when missles are available.
        #   Prio higher expected hits targets.

        # Add penalty for going over on assets
        if state["missiles"] < 0:
            reward -= 200

        if state ["assets"][0] < 0:
            reward -= 200

        if state ["assets"][1] < 0:
            reward -= 200

        isExpectedDamageMet = True
        for shipIndex in range(0, numberOfTargets):
            if state["currentShipDamage"][shipIndex] < state["expectedShipDamage"][shipIndex]:
                isExpectedDamageMet = False
                break

        if isExpectedDamageMet:
            reward += 100
            reward += max(0, state["missiles"])*10
            reward += max(0, state["assets"][0])*5
            reward += max(0, state["assets"][1])*5
            done = True

        if state["missiles"] <= 0:
            done = True

        if state["assets"][0] <= 0 or state["assets"][1] <= 0:
            done = True
        
        # Return step information
        return state, reward, done, info

class DeterministicScenarioEnvironment(Env):
    def __init__(self, numberOfmissiles, numberOfJets, numberOfPilots, tD1, tD2, tD3, tD4, tD5, tD6):
        manager = DeterministicScenario()
        self.manager = manager
        # Actions we can take: 0 - Do Nothing, 1 - Launch
        self.action_space = manager.getActionSpace()
        # Target Damage state array: 0 - Untouched, 1 - Disabled, 2 - Destroyed
        self.observation_space = manager.getObservationSpace()
        # store initial state
        self.numberOfmissiles = numberOfmissiles
        self.numberOfJets = numberOfJets
        self.numberOfPilots = numberOfPilots
        self.tD1 = tD1
        self.tD2 = tD2
        self.tD3 = tD3
        self.tD4 = tD4
        self.tD5 = tD5
        self.tD6 = tD6
        # Set start state
        self.state = self.manager.getState(self.numberOfmissiles, self.numberOfJets, self.numberOfPilots, self.tD1, self.tD2, self.tD3, self.tD4, self.tD5, self.tD6)

    def step(self, action):
        # Return step information
        return self.manager.step(self.state, action)

    def render(self):
        # Implement viz
        pass

    def reset(self):
        # Reset shower temperature
        self.state = self.manager.getState(self.numberOfmissiles, self.numberOfJets, self.numberOfPilots, self.tD1, self.tD2, self.tD3, self.tD4, self.tD5, self.tD6)
        return self.state

def shootShip(currentDamage):
    newDamage = currentDamage
    roll = random.randint(0, 100)
    if roll <= 60:
        # Should we reward more here?
        newDamage = max(1, currentDamage)
    
        roll = random.randint(0, 100)
        if roll <= 50:
            # Should we reward more here?
            newDamage = max(2, currentDamage)
    return newDamage

def simulate(model, numberOfMissiles, numberOfJets, numberOfPilots, damage1, damage2, damage3, damage4, damage5, damage6, confidence = 2):
    scenarioEnvironment = DeterministicScenarioEnvironment(numberOfMissiles, numberOfJets, numberOfPilots, damage1*confidence, damage2*confidence, damage3*confidence, damage4*confidence, damage5*confidence, damage6*confidence)
    observation = scenarioEnvironment.reset()

    predictions = []
    damageArray = [damage1, damage2, damage3, damage4, damage5, damage6]
    solvedArray = [0, 0, 0, 0, 0, 0]

    for x in range(0, 100+1):
        sorties = []
        done = False
        observation = scenarioEnvironment.reset()

        while not done:
            action, _ = model.predict(observation)
            observation, _, done, _ = scenarioEnvironment.step(action)
            sorties.append([action.tolist(), [observation["missiles"], 
            observation["expectedShipDamage"].tolist(), 
            observation["currentShipDamage"].tolist(), 
            observation["assets"].tolist()]])

        solved = 0
        solvedArray = [0, 0, 0, 0, 0, 0]
        for x in range(0, 1000):
            observation = scenarioEnvironment.reset()
            for sortie in sorties:
                observation, _, done, _ = scenarioEnvironment.step(sortie[0])
            
            isExpectedDamageMet = True
            for shipIndex in range(0, 6):
                damage = 0
                for shot in range(0, observation["currentShipDamage"][shipIndex]):
                    damage = shootShip(damage)

                if damage < damageArray[shipIndex]:
                    solvedArray[shipIndex] += 1
                    isExpectedDamageMet = False
                    break

            if isExpectedDamageMet and observation["missiles"] >= 0 and observation["assets"][0] >=0 and observation["assets"][1] >= 0:
                solved += 1
        predictions.append([(solved/1000.0)*100, solvedArray, sorties])

    predictions.sort(reverse=True, key=lambda p: p[0])
    scenarioEnvironment.close()

    predictionResults = []

    for prediction in predictions[0:1]:
        actions = []
        for sortie in prediction[2]:
            sortieResult = {"Actions":sortie[0], "Missiles": sortie[1][0], "ExpectedHits": sortie[1][1], "CurrentHits": sortie[1][2], "Assets": sortie[1][3]}
            actions.append(sortieResult)
        
        predictionResult = {"SuccessRate": prediction[0], "TargetRates": prediction[1], "Actions": actions}
        predictionResults.append(predictionResult)
    

    jsonResults = {"Results": predictionResults}

    return jsonResults