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
        reward = -100
        # Check if can attack
        for sorti in sortiArray:
            if state[sorti][ship1] and state[sorti][ship2]:
                canAttack = True
                reward = 2
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
                reward = -200
                shouldAttack = False
        else:
            # targetted a ship worth targetting
            reward = 50
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
    def shootShip(self, state, ship):
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

        canAttack , canAttackReward = self.canAttack(state, sortieArray, ship1Index, ship2Index)

        if canAttack:
            shouldAttack, shouldAttackReward1 = self.shouldAttack(state, sortieArray, ship1Index)
            shouldAttack2, shouldAttackReward2 = self.shouldAttack(state, sortieArray, ship2Index)

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

            self.shootShip(state, ship1Index)
            state["missiles"] -= 1
            if action[2] == 1:
                self.shootShip(state, ship1Index)
                state["missiles"] -= 1
            self.shootShip(state, ship2Index)
            state["missiles"] -= 1
            if action[3] == 1:
                self.shootShip(state, ship2Index)
                state["missiles"] -= 1

            reward = canAttackReward + shouldAttackReward1 + shouldAttackReward2
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
            reward += 300
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

class TrainingDeterministicScenarioEnvironment(Env):
    def __init__(self):
        manager = DeterministicScenario()
        self.manager = manager
        # Actions we can take: 0 - Do Nothing, 1 - Launch
        self.action_space = manager.getActionSpace()
        # Target Damage state array: 0 - Untouched, 1 - Disabled, 2 - Destroyed
        self.observation_space = manager.getObservationSpace()
        # Set start state
        self.state = manager.getRandomizedState()

    def step(self, action):
        # Return step information
        return self.manager.step(self.state, action)

    def render(self):
        # Implement viz
        pass

    def reset(self):
        # Reset shower temperature
        self.state = self.manager.getRandomizedState()
        return self.state
