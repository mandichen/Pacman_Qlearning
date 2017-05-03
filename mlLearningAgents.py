# python 2.7 script
# Chen/13-apr-2017
# based on the script written by Parsons
#
#
# A stub for a reinforcement learning agent to work with the Pacman
# piece of the Berkeley AI project:
#
# http://ai.berkeley.edu/reinforcement.html
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
import random
import math
import game
import util

# QLearnAgent
#
class QLearnAgent(Agent):

    # Constructor, called when we start running the
    def __init__(self, alpha=0.2, epsilon=0.05, gamma=0.8, numTraining = 10):
        # alpha       - learning rate
        # epsilon     - exploration rate
        # gamma       - discount factor
        # numTraining - number of training episodes
        #
        # These values are either passed from the command line or are
        # set to the default values above. We need to create and set
        # variables for them
        self.alpha = float(alpha)
        self.epsilon = float(epsilon)
        self.gamma = float(gamma)
        self.numTraining = int(numTraining)
        # Count the number of games we have played
        self.episodesSoFar = 0
        # Q-values
        self.q_value = util.Counter()
        # current score
        self.score = 0
        # last state
        self.lastState = []
        # last action
        self.lastAction = []



    # Accessor functions for the variable episodesSoFars controlling learning
    def incrementEpisodesSoFar(self):
        self.episodesSoFar +=1

    def getEpisodesSoFar(self):
        return self.episodesSoFar

    def getNumTraining(self):
            return self.numTraining

    # Accessor functions for parameters
    def setEpsilon(self, value):
        self.epsilon = value

    def getAlpha(self):
        return self.alpha

    def setAlpha(self, value):
        self.alpha = value

    def getGamma(self):
        return self.gamma

    def getMaxAttempts(self):
        return self.maxAttempts

    # functions for calculation
    # get Q(s,a)
    def getQValue(self, state, action):
        return self.q_value[(state,action)]

    # return the maximum Q of state
    def getMaxQ(self, state):
        q_list = []
        for a in state.getLegalPacmanActions():
            q = self.getQValue(state,a)
            q_list.append(q)
        if len(q_list) ==0:
            return 0
        return max(q_list)

    # update Q value
    def updateQ(self, state, action, reward, qmax):
        q = self.getQValue(state,action)
        self.q_value[(state,action)] = q + self.alpha*(reward + self.gamma*qmax - q)

    # return the action maximises Q of state
    def doTheRightThing(self, state):
        legal = state.getLegalPacmanActions()
        # in the first half of trianing, the agent is forced not to stop
        # or turn back while not being chased by the ghost
        if self.getEpisodesSoFar()*1.0/self.getNumTraining()<0.5:
            if Directions.STOP in legal:
                legal.remove(Directions.STOP)
            if len(self.lastAction) > 0:
                last_action = self.lastAction[-1]
                distance0 = state.getPacmanPosition()[0]- state.getGhostPosition(1)[0]
                distance1 = state.getPacmanPosition()[1]- state.getGhostPosition(1)[1]
                if math.sqrt(distance0**2 + distance1**2) > 2:
                    if (Directions.REVERSE[last_action] in legal) and len(legal)>1:
                        legal.remove(Directions.REVERSE[last_action])
        tmp = util.Counter()
        for action in legal:
          tmp[action] = self.getQValue(state, action)
        return tmp.argMax()

    # getAction
    #
    # The main method required by the game. Called every time that
    # Pacman is expected to move
    def getAction(self, state):

        # The data we have about the state of the game
        # the legal action of this state
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        # update Q-value
        reward = state.getScore()-self.score
        if len(self.lastState) > 0:
            last_state = self.lastState[-1]
            last_action = self.lastAction[-1]
            max_q = self.getMaxQ(state)
            self.updateQ(last_state, last_action, reward, max_q)

        # e-greedy
        if util.flipCoin(self.epsilon):
            action =  random.choice(legal)
        else:
            action =  self.doTheRightThing(state)

        # update attributes
        self.score = state.getScore()
        self.lastState.append(state)
        self.lastAction.append(action)

        return action

    # Handle the end of episodes
    #
    # This is called by the game after a win or a loss.
    def final(self, state):

        # update Q-values
        reward = state.getScore()-self.score
        last_state = self.lastState[-1]
        last_action = self.lastAction[-1]
        self.updateQ(last_state, last_action, reward, 0)

        # reset attributes
        self.score = 0
        self.lastState = []
        self.lastAction = []

        # decrease epsilon during the trianing
        ep = 1 - self.getEpisodesSoFar()*1.0/self.getNumTraining()
        self.setEpsilon(ep*0.1)


        # Keep track of the number of games played, and set learning
        # parameters to zero when we are done with the pre-set number
        # of training episodes
        self.incrementEpisodesSoFar()
        if self.getEpisodesSoFar() % 100 == 0:
            print "Completed %s runs of training" % self.getEpisodesSoFar()

        if self.getEpisodesSoFar() == self.getNumTraining():
            msg = 'Training Done (turning off epsilon and alpha)'
            print '%s\n%s' % (msg,'-' * len(msg))
            self.setAlpha(0)
            self.setEpsilon(0)
