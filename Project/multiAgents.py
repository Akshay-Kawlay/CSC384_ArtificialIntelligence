# multiAgents.py
# --------------
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
import math
import datetime

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
          Here are some method calls that might be useful when implementing minimax.
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        Score, wiseMove = self.getActionH(gameState, self.depth, 0)
        return wiseMove

    def getActionH(self, gameState, depth, agentIndex):
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), None
        Scores = []
        
        if agentIndex != 0:
            legalActions = gameState.getLegalActions(agentIndex)
        
        if agentIndex == 0:
            legalActions = gameState.getLegalActions()
            Scores = [self.getActionH(gameState.generateSuccessor(self.index, action), depth, 1) for action in legalActions]
            wanted_score = max(Scores)
            
        elif (agentIndex == gameState.getNumAgents()-1):
            Scores = [self.getActionH(gameState.generateSuccessor(agentIndex, action), depth-1, 0) for action in legalActions]
            wanted_score = min(Scores)
           
        else:
            Scores = [self.getActionH(gameState.generateSuccessor(agentIndex, action), depth, agentIndex+1) for action in legalActions]
            wanted_score = min(Scores)
        
        for i in range(len(Scores)):
            if Scores[i] == wanted_score:
                wanted_index = i
                break
        
        return wanted_score, legalActions[wanted_index]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        action = Directions.STOP
        alpha = float('-inf')
        beta = float('inf')
        score, wiseAction = self.getActionH(gameState, self.depth, 0, action, alpha, beta)
        return wiseAction

    def getActionH(self, gameState, depth, agentIndex, action, alpha, beta):
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), action
        
        if agentIndex != 0:
            legalActions = gameState.getLegalActions(agentIndex)
#             if Directions.STOP in legalActions:
#                 legalActions.remove(Directions.STOP)
        
        previousAction = Directions.STOP
        if agentIndex == 0:
            legalActions = gameState.getLegalActions()
            node_val = float('-inf')
#             if Directions.STOP in legalActions:
#                 legalActions.remove(Directions.STOP)
            for action in legalActions:
                temp_val, currentAction = self.getActionH(gameState.generateSuccessor(agentIndex, action), depth, 1, action, alpha, beta)
                if temp_val > node_val:
                    previousAction = action
                    node_val = temp_val
                if node_val >= beta:
                    break
                alpha = max(alpha, node_val)
            
        else:
            node_val = float('inf')
            for action in legalActions:
                if agentIndex == gameState.getNumAgents()-1:
                    temp_val, currentAction = self.getActionH(gameState.generateSuccessor(agentIndex, action), depth-1, 0, action, alpha, beta)
                else:
                    temp_val, currentAction = self.getActionH(gameState.generateSuccessor(agentIndex, action), depth, agentIndex+1, action, alpha, beta)
                
                if temp_val < node_val:
                    previousAction = action
                    node_val = temp_val
                if node_val <= alpha:
                    break
                beta = min(node_val, beta)
           
        return node_val, previousAction 

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        legalActions = gameState.getLegalActions()
        scores = [self.getActionH(gameState.generateSuccessor(0, action), self.depth, 1) for action in legalActions]
        max_score = max(scores)
        max_index = [i for i in range(len(scores)) if scores[i] == max_score]
        return legalActions[max_index[0]]

    def getActionH(self, gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
            
        if agentIndex != 0:
            legalActions = gameState.getLegalActions(agentIndex)
            
        if agentIndex == 0:
            legalActions = gameState.getLegalActions()
            Scores = [self.getActionH(gameState.generateSuccessor(agentIndex, action), depth, 1) for action in legalActions]
            return max(Scores)
            
        elif (agentIndex == gameState.getNumAgents()-1):
            Scores = [self.getActionH(gameState.generateSuccessor(agentIndex, action), depth-1, 0) for action in legalActions]
            return sum(Scores)/len(legalActions)
           
        else:
            Scores = [self.getActionH(gameState.generateSuccessor(agentIndex, action), depth, agentIndex+1) for action in legalActions]
            return sum(Scores)/len(legalActions)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <The pacman's has to survive so it runs away from ghosts while getting higher score, so the two things are combineds>
    """
    "*** YOUR CODE HERE ***"
    #finding minimum manhattan distance from ghosts
    min = float('inf')
    xy1 = currentGameState.getPacmanPosition()
    for i in currentGameState.getNumAgents()-1:
        if i != 0:
            xy2 = currentGameState.getGhostPosition(i)
            manDist = manhattanDistance(xy1,xy2)
            if manDist < min:
                min = manDist
            
    return currentGameState.getScore()+ min*min

# Abbreviation
better = betterEvaluationFunction

#from MonteCarloAgent-fixes.txt--------------------------------------------------------

# add the function scoreEvaluationFunction to multiAgents.py
def scoreEvaluationFunction(currentGameState):
   """
     This default evaluation function just returns the score of the state.
     The score is the same one displayed in the Pacman GUI.

     This evaluation function is meant for use with adversarial search agents
   """
   return currentGameState.getScore()

# add this class to multiAgents.py
# the following class corrects and replaces the previous MonteCarloAgent class released on March 19
# the only differences between this version, and the one released on March 19 are:
#       * line 37 of this file, "if self.Q" has been replaced by "if Q"
#       * line 45 of this file, where "assert( Q == 'contestClassic' )" has been added
class MonteCarloAgent(MultiAgentSearchAgent):
    """
        Your monte-carlo agent (question 5)
        ***UCT = MCTS + UBC1***
        TODO:
        1) Complete getAction to return the best action based on UCT.
        2) Complete runSimulation to simulate moves using UCT.
        3) Complete final, which updates the value of each of the states visited during a play of the game.

        * If you want to add more functions to further modularize your implementation, feel free to.
        * Make sure that your dictionaries are implemented in the following way:
            -> Keys are game states.
            -> Value are integers. When performing division (i.e. wins/plays) don't forget to convert to float.
      """

    def __init__(self, evalFn='mctsEvalFunction', depth='-1', timeout='50', numTraining=100, C='2', Q=None):
        # This is where you set C, the depth, and the evaluation function for the section "Enhancements for MCTS agent".
        if Q:
            if Q == 'minimaxClassic':
                self.C = 2
                depth=4
                pass
            elif Q == 'testClassic':
                self.C = 2
                depth=4
                pass
            elif Q == 'smallClassic':
                self.C = 2
                depth=3
                pass
            else: # Q == 'contestClassic'
                self.C = 2
                depth=5
                assert( Q == 'contestClassic' )
                pass
        # Otherwise, your agent will default to these values.
        else:
            self.C = int(C)
            # If using depth-limited UCT, need to set a heuristic evaluation function.
            if int(depth) > 0:
                evalFn = 'scoreEvaluationFunction'
        self.states = []
        self.plays = dict()
        self.wins = dict()
        self.calculation_time = datetime.timedelta(milliseconds=int(timeout))

        self.numTraining = numTraining

        "*** YOUR CODE HERE ***"

        MultiAgentSearchAgent.__init__(self, evalFn, depth)

    def update(self, state):
        """
        You do not need to modify this function. This function is called every time an agent makes a move.
        """
        self.states.append(state)

    def getAction(self, gameState):
        """
        Returns the best action using UCT. Calls runSimulation to update nodes
        in its wins and plays dictionary, and returns best successor of gameState.
        """
        "*** YOUR CODE HERE ***"
        
        games = 0
        begin = datetime.datetime.utcnow()
        self.plays[gameState] = 0
        self.wins[gameState] = 0
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            games += 1
            self.run_simulation(gameState)
            
        #self calculation
        max = float('-inf')
        Vi = float('-inf')
        legalActions = gameState.getLegalActions(0)
        for action in legalActions:
            child = gameState.generateSuccessor(0, action)
            Vi = float(self.wins[child]/self.plays[child])
            if Vi > max:
                max = Vi
                bestAction = action
                
        
        return bestAction
        
        
    def run_simulation(self, state):
        """
        Simulates moves based on MCTS.
        1) (Selection) While not at a leaf node, traverse tree using UCB1.
        2) (Expansion) When reach a leaf node, expand.
        4) (Simulation) Select random moves until terminal state is reached.
        3) (Backpropapgation) Update all nodes visited in search tree with appropriate values.
        * Remember to limit the depth of the search only in the expansion phase!
        Updates values of appropriate states in search with with evaluation function.
        """
        "*** YOUR CODE HERE ***"
        #selection
        parent_state = None
        temp_state = state
        visited = []
        agentIndex = 0
        if temp_state not in self.plays:
            self.plays[temp_state] = 0
            self.wins[temp_state] = 0

        while (temp_state in self.plays):
            legalActions = temp_state.getLegalActions(agentIndex)
            if len(legalActions) == 0: #terminal state has been reached
                return
            successors = [temp_state.generateSuccessor(agentIndex, action) for action in legalActions]
            max_UCB1 = max([self.UCB1(successors[i], temp_state) for i in range(len(successors))])
            for i in range(len(successors)):
                if self.UCB1(successors[i], temp_state) == max_UCB1:
                    parent_state = temp_state
                    temp_state = successors[i]
                    break
            if agentIndex == temp_state.getNumAgents()-1:
                agentIndex = 0
            else:
                agentIndex += 1
            if parent_state != None:
                visited.append(parent_state)
        
        #when while loop breaks when parent_state = a leaf node and temp_state is not yet explored
        #call for simulation (rollout)
        if self.plays[parent_state] == 0:
            val = self.rollout(parent_state, agentIndex)
        else:
            #expansion
            self.plays[temp_state] = 0
            self.wins[temp_state] = 0     
            val = self.rollout(temp_state, agentIndex)
            visited.append(temp_state)
        
        #backprop
        agentIndex = 0
        for node in visited:
            self.plays[node] += 1
            if agentIndex == 0:
                self.wins[node] = self.wins[node] + val
            else:
                self.wins[node] -= val
            if agentIndex == node.getNumAgents()-1:
                agentIndex = 0
            else:
                agentIndex += 1
                
       
    def UCB1(self, state, parent_state):
        if (state not in self.plays) or (self.plays[state] == 0):
            return float('inf')
        else:
            UCB1_val = float(self.wins[state]/self.plays[state]) + self.C * math.sqrt(float(math.log(self.plays[parent_state])/self.plays[state]))
        return UCB1_val
    
    #simulation    
    def rollout(self, state, agent):
        temp_state = state
        dep = int(self.depth)*(temp_state.getNumAgents())
        agentIndex = agent
        while(1):
            if dep == 0 or temp_state.isWin() or temp_state.isLose():
                if self.depth == -1:
                    return mctsEvalFunction(temp_state)
                else:
                    return scoreEvaluationFunction(temp_state)
                    
            legalActions = temp_state.getLegalActions(agentIndex)
            randomAction = random.choice(legalActions)
            random_successor = temp_state.generateSuccessor(agentIndex, randomAction)
            dep -= 1
            if agentIndex == temp_state.getNumAgents()-1:
                agentIndex = 0
            else:
                agentIndex += 1
            temp_state = random_successor
            
            
    def final(self, state):
        """
        Called by Pacman game at the terminal state.
        Updates search tree values of states that were visited during an actual game of pacman.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

def mctsEvalFunction(state):
    """
    Evaluates state reached at the end of the expansion phase.
    """
    return 1 if state.isWin() else 0
