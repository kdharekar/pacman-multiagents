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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFoodList = newFood.asList()
        min_food_dist = float("inf")
        for food_item in newFoodList:
            if(manhattanDistance(food_item,newPos)<min_food_dist):
                min_food_dist=manhattanDistance(food_item,newPos)
        ghostDistance = float("inf")
        for ghost in successorGameState.getGhostPositions():
            if(manhattanDistance(ghost,newPos)<=1):
                return -float("inf")
            elif(manhattanDistance(ghost,newPos)<ghostDistance):
                ghostDistance=manhattanDistance(ghost,newPos)
            
        return successorGameState.getScore() + 1.0/min_food_dist - 1.0/ghostDistance

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        answer = self.getAnswer(0,gameState,0)[1]
        return answer
    def getAnswer(self,AgentIndex,gameState,depth):
        if(self.depth==depth or len(gameState.getLegalActions(AgentIndex)) == 0 or gameState.isLose() or gameState.isWin() ):
            return self.evaluationFunction(gameState),""
        if(AgentIndex==0):
            return self.MaxFun(AgentIndex,gameState,depth)
        else:
            return self.MinFun(AgentIndex,gameState,depth)

    def MaxFun(self,AgentIndex,gameState,depth):
        ans = -float("inf")
        MaxAction = Directions.WEST
        for action in gameState.getLegalActions(AgentIndex):
            successor = gameState.generateSuccessor(AgentIndex, action)
            successor_Agent = AgentIndex+1
            succ_dpt = depth
            if(successor_Agent==gameState.getNumAgents()):
                successor_Agent = 0
                succ_dpt = succ_dpt + 1
            nextAns = self.getAnswer(successor_Agent,successor,succ_dpt)[0]
            if nextAns > ans:
                ans = nextAns
                MaxAction = action
        return ans,MaxAction
    
    def MinFun(self,AgentIndex,gameState,depth):
        MinAction = Directions.WEST
        ans = float("inf")
        for action in gameState.getLegalActions(AgentIndex):
            successor = gameState.generateSuccessor(AgentIndex, action)
            successor_Agent = AgentIndex+1
            succ_dpt = depth
            if(successor_Agent==gameState.getNumAgents()):
                successor_Agent = 0
                succ_dpt = succ_dpt + 1
            nextAns = self.getAnswer(successor_Agent,successor,succ_dpt)[0]
            if nextAns < ans:
                ans = nextAns
                MinAction = action
        return ans,MinAction
       




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        answer = self.getAnswer(0,gameState,0,-float("inf"),float("inf"))[1]
        return answer
    def getAnswer(self,AgentIndex,gameState,depth,alpha,beta):
        if(self.depth==depth or len(gameState.getLegalActions(AgentIndex)) == 0 or gameState.isLose() or gameState.isWin() ):
            return float(self.evaluationFunction(gameState)),""
        if(AgentIndex==0):
            return self.MaxFun(AgentIndex,gameState,depth,alpha,beta)
        else:
            return self.MinFun(AgentIndex,gameState,depth,alpha,beta)
    def MaxFun(self,AgentIndex,gameState,depth,alpha,beta):
        ans = -float("inf")
        MaxAction = Directions.WEST
        for action in gameState.getLegalActions(AgentIndex):
            successor = gameState.generateSuccessor(AgentIndex, action)
            successor_Agent = AgentIndex+1
            succ_dpt = depth

            if(successor_Agent==gameState.getNumAgents()):
                successor_Agent = 0
                succ_dpt = succ_dpt + 1

            nextAns = self.getAnswer(successor_Agent,successor,succ_dpt,alpha,beta)[0]
            
            if nextAns > ans:
                ans = nextAns
                MaxAction = action
            alpha = max(alpha, ans)
            if alpha > beta:
                return  ans,MaxAction
        return ans,MaxAction
    def MinFun(self,AgentIndex,gameState,depth,alpha,beta):
        ans = float("inf")
        MinAction = Directions.WEST
        for action in gameState.getLegalActions(AgentIndex):
            successor = gameState.generateSuccessor(AgentIndex, action)
            successor_Agent = AgentIndex+1
            succ_dpt = depth

            if(successor_Agent==gameState.getNumAgents()):
                successor_Agent = 0
                succ_dpt = succ_dpt + 1

            nextAns = float(self.getAnswer(successor_Agent,successor,succ_dpt,alpha,beta)[0])
            
            if  ans > nextAns:
                ans = nextAns
                MinAction = action

            beta = min(beta, ans)
            if alpha > beta:
                return  ans,MinAction
        return ans,MinAction

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
