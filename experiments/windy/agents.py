import random

from multiagentrl import core
from multiagentrl import exploration
from multiagentrl import learning


class RandomAgent(core.BaseControllerAgent):
    """Agent that randomly selects an action."""
    def __init__(self, agent_id, ally_ids, enemy_ids):
        super(RandomAgent, self).__init__(agent_id)

    def learn(self, state, action, reward):
        pass

    def act(self, state, legal_actions, explore):
        if legal_actions:
            return random.choice(legal_actions)


class LearningAgent(core.BaseControllerAgent):
    def __init__(self, agent_id, ally_ids, enemy_ids):
        super(LearningAgent, self).__init__(agent_id)
        self.K = 1.0  # Learning rate
        self.iteration = 1
        self.exploration_rate = 0.1
        self.learning = learning.QLearning(
            learning_rate=0.1, discount_factor=0.9, actions=range(4))
        self.exploration = exploration.EGreedy(
            exploration_rate=self.exploration_rate)

    def get_policy(self):
        return self.learning.q_values

    def set_policy(self, weights):
        self.learning.q_values = weights

    def learn(self, state, action, reward):
        self.learning.learning_rate = self.K / (self.K + self.iteration)
        self.learning.learn(state, action, reward)
        self.iteration += 1

    def act(self, state, legal_actions, explore):
        action = self.learning.act(state)

        if explore:
            return self.exploration.explore(action, legal_actions)
        else:
            return action

    def enable_learn_mode(self):
        self.learning.exploration_rate = self.exploration_rate

    def enable_test_mode(self):
        self.learning.exploration_rate = 0
