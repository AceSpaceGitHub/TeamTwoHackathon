from gym import Env

from scenario_manager import ScenarioManager

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
