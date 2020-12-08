# import Agent
import random
# import agent.ProbAgent as agent_file
# import random
import numpy as np


class Orientation():
    def __init__(self,current_orientation):
        self.current_orientation = current_orientation
    def turnLeft(self):
        if self.current_orientation == 'North':
            return 'West'
        if self.current_orientation == 'South':
            return 'East'
        if self.current_orientation == 'West':
            return 'South'
        if self.current_orientation == 'East':
            return 'North'
    def turnRight(self):
        if self.current_orientation == 'North':
            return 'East'
        if self.current_orientation == 'South':
            return 'West'
        if self.current_orientation == 'West':
            return 'North'
        if self.current_orientation == 'East':
            return 'South'

class Percept():
    def __init__(self, stench, breeze, glitter, bump, scream, isTerminated, reward):
        self.stench = stench
        self.breeze = breeze
        self.glitter = glitter
        self.bump = bump
        self.scream = scream
        self.isTerminated = isTerminated
        self.reward = reward
    def show(self):
        string = ('Stench:' + str(self.stench) + ', Breeze:' + str(self.breeze) + ', Glitter:' + str(self.glitter) +
                ', Bump:' + str(self.bump) +
                ', Scream:' + str(self.scream) +
                ', Isterminated:' + str(self.isTerminated) + ', Reward:' + str(self.reward))
        return string

# class Agent():
#     def __init__(self, Coords = (0,0), Orientation = 'East', HasGold = False, HasArrow = True, IsAlive = True):
#         self.coords = Coords
#         self.orientation = Orientation
#         self.hasgold = HasGold
#         self.hasarrow = HasArrow
#         self.isalive = IsAlive
#     def turnLeft(self):
#         self.orientation = Orientation(self.orientation).turnLeft()
#         return self
#     def turnRight(self):
#         self.orientation = Orientation(self.orientation).turnRight()
#         return self
#     def forward(self,gridWidth,gridHeight):
#         if self.orientation == 'West':
#             self.coords = (max(0, self.coords[0]-1), self.coords[1])
#         if self.orientation == 'East':
#             self.coords = (min(gridWidth-1, self.coords[0]+1), self.coords[1])
#         if self.orientation == 'South':
#             self.coords = (self.coords[0], max(0, self.coords[1]-1))
#         if self.orientation == 'North':
#             self.coords = (self.coords[0], min(gridHeight-1, self.coords[1]+1))
#         return self
    
class AgentState():
    def __init__(self, Coords = (0,0), Orientation = 'East', HasGold = False, HasArrow = True, IsAlive = True, WumpusAlive = True,
                 beelineActionList=[],
                 stenchLocations = [],
                 breezeLocations = [],
                 visitedLocations = [(0,0)],
                 previousActions = [],
                 previousLocations = [(0,0)],
                 repeatFeat = [0,0],
                 recentReward = 0,
                 totalReward = 0):
        self.coords = Coords
        self.orientation = Orientation
        self.hasgold = HasGold
        self.hasarrow = HasArrow
        self.isalive = IsAlive
        self.beelineactionlist = beelineActionList
        self.stenchlocations = stenchLocations
        self.breezelocations = breezeLocations
        self.visitedlocations = visitedLocations
        self.wumpusalive = WumpusAlive
        self.recentreward = recentReward
        self.totalreward = totalReward
        self.previousactions = previousActions
        self.previouslocations = previousLocations
        self.repeatfeat = repeatFeat
    def turnLeft(self):
        self.orientation = Orientation(self.orientation).turnLeft()
        return self
    def turnRight(self):
        self.orientation = Orientation(self.orientation).turnRight()
        return self
    def forward(self,gridWidth,gridHeight):
        if self.orientation == 'West':
            self.coords = (max(0, self.coords[0]-1), self.coords[1])
        if self.orientation == 'East':
            self.coords = (min(gridWidth-1, self.coords[0]+1), self.coords[1])
        if self.orientation == 'South':
            self.coords = (self.coords[0], max(0, self.coords[1]-1))
        if self.orientation == 'North':
            self.coords = (self.coords[0], min(gridHeight-1, self.coords[1]+1))
        self.visitedlocations.append(self.coords)
        self.visitedlocations = list(set(self.visitedlocations))
        return self
    
    def applyMoveAction(self,Action,gridWidth,gridHeight):
        if Action == 'TurnLeft':
            return self.turnleft()
        if Action == 'TurnRight':
            return self.turnRight()
        if Action == 'Forward':
            return self.forward(gridWidth,gridHeight)
        return self
        


        
class Environment():
    def __init__(self,gridWidth=4, gridHeight=4, pitProb=0.2, allowClimbwithoutGold=True, 
                 agent = AgentState(),#agent_file.BeelineAgent().agentstate, 
                 pitLocations=[],
                 terminated=False,
                 wumpusLocation = (0,0),
                 wumpusAlive=True, 
                 goldLocation=(0,0),
                 BeliefState = []):
        self.gridwidth = gridWidth
        self.gridheight = gridHeight
        self.pitprob = pitProb
        self.allowclimbwithoutgold = allowClimbwithoutGold
        self.agent = agent
        self.pitlocations = pitLocations
        self.terminated = terminated
        self.wumpuslocation = wumpusLocation
        self.wumpusalive = wumpusAlive
        self.goldlocation = goldLocation
        self.beliefstate = BeliefState
    def isPitAt(self,pitcoords):
        return pitcoords in self.pitlocations
    def isWumpusAt(self,wumcoords):
        return wumcoords == self.wumpuslocation
    def isAgentAt(self,agentcoords):
        return agentcoords == self.agent.coords
    def isGlitter(self):
        return self.goldlocation == self.agent.coords
    def isGoldAt(self,goldcoords):
        return goldcoords == self.goldlocation
    def wumpusInLineOfFire(self):
        if self.agent.orientation == 'West':
            result = (self.agent.coords[0] > self.wumpuslocation[0]) & (self.agent.coords[1] == self.wumpuslocation[1])
            return result
        if self.agent.orientation == 'East':
            result = (self.agent.coords[0] < self.wumpuslocation[0]) & (self.agent.coords[1] == self.wumpuslocation[1])
            return result
        if self.agent.orientation == 'South':
            result = (self.agent.coords[0] == self.wumpuslocation[0]) & (self.agent.coords[1] > self.wumpuslocation[1])
            return result
        if self.agent.orientation == 'North':
            result =  (self.agent.coords[0] == self.wumpuslocation[0]) & (self.agent.coords[1] < self.wumpuslocation[1])
            return result
    def killAttemptSuccessful(self):
        result = self.wumpusInLineOfFire() and self.wumpusalive and self.agent.hasarrow
        return result
    def adjacentCells(self, coords):
        adj_coords = []
        if coords[0]>0: #left
            adj_coords.append((coords[0]-1,coords[1]))
        else:
            adj_coords.append(None)
        if coords[0]<(self.gridwidth-1): #right
            adj_coords.append((coords[0]+1,coords[1]))
        else:
            adj_coords.append(None)
        if coords[1]>0: #below
            adj_coords.append((coords[0],coords[1]-1))
        else:
            adj_coords.append(None)
        if coords[1]<(self.gridheight-1): #up
            adj_coords.append((coords[0],coords[1]+1))
        else:
            adj_coords.append(None)
        return adj_coords
        # [left right below above]
        
    def isPitAdjacent(self, coords):
        for element in self.adjacentCells(coords):
            result = element in self.pitlocations
            if result == True:
                return result
        return result
    def isWumpusAdjacent(self, coords):
        for element in self.adjacentCells(coords):
            result = (element == self.wumpuslocation)
            if result == True:
                return result
        return result
    def isBreeze(self):
        return self.isPitAdjacent(self.agent.coords)
    def isStench(self):
        return self.isWumpusAdjacent(self.agent.coords)
    
    def applyAction(self,action,action_list = []):
        self.agent.beelineactionlist = action_list
        if self.terminated:
            env_class = Environment()
            percept_class = Percept(False, False, False, False, False, True, 0)
            return env_class,percept_class
        else:
            if action == 'Forward':
                current_coords = self.agent.coords
                movedAgent = self.agent.forward(self.gridwidth,self.gridheight)
                death = (self.isWumpusAt(movedAgent.coords) and self.wumpusalive) or self.isPitAt(movedAgent.coords)
                movedAgent.isalive = not death
                bumped = (movedAgent.coords == current_coords)
                newAgent_class = movedAgent
                self.agent.coords = movedAgent.coords
                self.agent = newAgent_class
                self.terminated = death
                self.goldlocation = newAgent_class.coords if self.agent.hasgold else self.goldlocation
                newEnv_class = self
                if newAgent_class.isalive:
                    percept_class = Percept(newEnv_class.isStench(), 
                                            newEnv_class.isBreeze(), 
                                            newEnv_class.isGlitter(), 
                                            bumped, 
                                            False, 
                                            not newAgent_class.isalive, 
                                            -1)
                else:
                    percept_class = Percept(newEnv_class.isStench(), 
                                            newEnv_class.isBreeze(), 
                                            newEnv_class.isGlitter(), 
                                            bumped, 
                                            False, 
                                            not newAgent_class.isalive, 
                                            -1001)
                self.agent.currentreward = percept_class.reward
                self.agent.totalreward = self.agent.totalreward + self.agent.currentreward
                if newEnv_class.isStench():
                    self.agent.stenchlocations.append(self.agent.coords)
                    self.agent.stenchlocations = list(set(self.agent.stenchlocations))
                if newEnv_class.isBreeze():
                    self.agent.breezelocations.append(self.agent.coords)
                    self.agent.breezelocations = list(set(self.agent.breezelocations))
                self.agent.previousactions.append('Forward')
                self.agent.previouslocations.append(self.agent.coords)
                newEnv_class = self
                
                return newEnv_class,percept_class
            if action == 'TurnLeft':
                self.agent = self.agent.turnLeft()
                percept_class = Percept(self.isStench(), 
                                        self.isBreeze(), 
                                        self.isGlitter(), 
                                        False, 
                                        False, 
                                        False, 
                                        -1)
                self.agent.currentreward = percept_class.reward
                self.agent.totalreward = self.agent.totalreward + self.agent.currentreward
                self.agent.previousactions.append('TurnLeft')
                self.agent.previouslocations.append(self.agent.coords)
                newEnv_class = self
                return newEnv_class,percept_class
            if action == 'TurnRight':
                self.agent = self.agent.turnRight()
                percept_class = Percept(self.isStench(), 
                                        self.isBreeze(), 
                                        self.isGlitter(), 
                                        False, 
                                        False, 
                                        False, 
                                        -1)
                self.agent.currentreward = percept_class.reward
                self.agent.totalreward = self.agent.totalreward + self.agent.currentreward
                self.agent.previousactions.append('TurnRight')
                self.agent.previouslocations.append(self.agent.coords)
                newEnv_class = self
                return newEnv_class,percept_class
            if action == 'Grab':
                self.agent.hasgold = self.isGlitter()
                newAgent_class = self.agent
                self.agent = newAgent_class
                self.goldlocation = newAgent_class.coords if newAgent_class.hasgold else self.goldlocation
                newEnv_class = self
                percept_class = Percept(self.isStench(), 
                                        self.isBreeze(), 
                                        self.isGlitter(), 
                                        False, 
                                        False, 
                                        False, 
                                        -1)
                self.agent.currentreward = percept_class.reward
                self.agent.totalreward = self.agent.totalreward + self.agent.currentreward
                self.agent.previousactions.append('Grab')
                self.agent.previouslocations.append(self.agent.coords)
                newEnv_class = self
                return newEnv_class,percept_class
            if action == 'Climb':
                inStartLocation = (self.agent.coords==(0,0))
                success = self.agent.hasgold and inStartLocation
                isTerminated = (success or self.allowclimbwithoutgold) and inStartLocation
                self.terminated = isTerminated
                newEnv_class = self
                if success:
                    percept_class = Percept(False, 
                                            False, 
                                            self.agent.hasgold, 
                                            False, 
                                            False, 
                                            isTerminated, 
                                            999)
                else:
                    if inStartLocation:
                        percept_class = Percept(False, 
                                                False, 
                                                self.agent.hasgold, 
                                                False, 
                                                False, 
                                                isTerminated,
                                                -1)
                    else:
                        percept_class = Percept(False, 
                                                False, 
                                                self.agent.hasgold, 
                                                False, 
                                                False, 
                                                isTerminated,
                                                -1)
                self.agent.currentreward = percept_class.reward
                self.agent.totalreward = self.agent.totalreward + self.agent.currentreward
                self.agent.previousactions.append('Climb')
                self.agent.previouslocations.append(self.agent.coords)
                newEnv_class = self
                return newEnv_class,percept_class
            if action == 'Shoot':
                hadArrow = self.agent.hasarrow
                wumpusKilled = self.killAttemptSuccessful()
                if hadArrow:
                    self.agent.wumpusalive = not wumpusKilled
                    self.agent.hasarrow = False
                    newAgent_class = self.agent
                    self.agent = newAgent_class
                    self.wumpusalive = not wumpusKilled
                    newEnv_class = self
                    percept_class = Percept(self.isStench(), 
                                            self.isBreeze(), 
                                            self.isGlitter(), 
                                            False, 
                                            wumpusKilled, 
                                            False, 
                                            -11)
                else:
                    newEnv_class = self
                    percept_class = Percept(self.isStench(), 
                                            self.isBreeze(), 
                                            self.isGlitter(), 
                                            False, 
                                            wumpusKilled, 
                                            False, 
                                            -1)
                self.agent.currentreward = percept_class.reward
                self.agent.totalreward = self.agent.totalreward + self.agent.currentreward
                self.agent.previousactions.append('Shoot')
                self.agent.previouslocations.append(self.agent.coords)
                newEnv_class = self
                return newEnv_class,percept_class
    
    def visualize(self):
        wumpusSymbol = 'W' if self.wumpusalive else 'w'
        string=''
        length=4
        for y in range(self.gridheight-1,-1,-1):
            for x in range(0,self.gridwidth,1):
                row = ''
                if x < 3:
                    if self.isAgentAt((x,y)):
                        row += "A"  
                    if self.isPitAt((x,y)):
                        row += "P"
                    if self.isWumpusAt((x,y)): 
                        row += wumpusSymbol
                    if self.isGoldAt((x,y)):
                        row += "G"
                    for i in range(length):
                        if len(row) == i:
                            row += " " * (length-i) + "|"
                if x==3:
                    if self.isAgentAt((x,y)):
                        row += "A"  
                    if self.isPitAt((x,y)):
                        row += "P"
                    if self.isWumpusAt((x,y)): 
                        row += wumpusSymbol
                    if self.isGoldAt((x,y)):
                        row += "G"
                    for i in range(length):
                        if len(row) == i:
                            row += " " * (length-i) + "\n"
                string += row    
        return string
    
    def render_np(self):
        GW = self.gridwidth
        GH = self.gridheight
        stench_feat = np.zeros((self.gridheight,self.gridwidth))
        breeze_feat = np.zeros((self.gridheight,self.gridwidth))
        visited_feat = np.zeros((self.gridheight,self.gridwidth))
        agentloc_feat = np.zeros((self.gridheight,self.gridwidth))
        orientation_list = np.array(['East','South','West','North'])
#         orientation = self.agent.orientation
#         orientation_feat = 1.*(orientation_list == orientation)
        stench_list = np.array(self.agent.stenchlocations)
        breeze_list = np.array(self.agent.breezelocations)
        visited_list = np.array(self.agent.visitedlocations)
        agent_location = self.agent.coords
        if self.agent.stenchlocations!= []:
            stench_feat[tuple(stench_list.T)]=1.
        if self.agent.breezelocations!=[]:
            breeze_feat[tuple(breeze_list.T)]=1.
        if self.agent.visitedlocations!=[]:
            visited_feat[tuple(visited_list.T)]=1.
        
        
        agentloc_feat[agent_location]=1.
        hasgold_feat = np.ones((self.gridheight,self.gridwidth)) if self.agent.hasgold else np.zeros((self.gridheight,self.gridwidth))
        glitter_feat = np.ones((self.gridheight,self.gridwidth)) if self.isGlitter() else np.zeros((self.gridheight,self.gridwidth))
        hasarrow_feat = np.ones((self.gridheight,self.gridwidth)) if self.agent.hasarrow else np.zeros((self.gridheight,self.gridwidth))
        scream_feat = np.zeros((self.gridheight,self.gridwidth)) if self.agent.wumpusalive else np.ones((self.gridheight,self.gridwidth))
        agentloc_feat = np.rot90(agentloc_feat)
        visited_feat = np.rot90(visited_feat)
        stench_feat = np.rot90(stench_feat)
        breeze_feat = np.rot90(breeze_feat)
        
        orientation_feat = np.zeros((4,GH,GW))
        if self.agent.orientation == 'East':
            orientation_feat[0] = np.ones((GH,GW))
        if self.agent.orientation == 'South':
            orientation_feat[1] = np.ones((GH,GW))
        if self.agent.orientation == 'West':
            orientation_feat[2] = np.ones((GH,GW))
        if self.agent.orientation == 'North':
            orientation_feat[3] = np.ones((GH,GW))
        
        repeat_feat = np.zeros((6,GH,GW))
        pre_actions = self.agent.previousactions
        pre_locations = self.agent.previouslocations
        if pre_actions:
            if pre_actions[-5:].count(pre_actions[-1]) == len(pre_actions[-5:]) and len(pre_actions[-5:])==5:
                repeat_feat[0]=np.ones((GH,GW))
                repeat_feat[1]=np.zeros((GH,GW))
                repeat_feat[2]=np.zeros((GH,GW))
                if pre_actions[-10:].count(pre_actions[-1]) == len(pre_actions[-10:]) and len(pre_actions[-10:])==10:
                    repeat_feat[0]=np.zeros((GH,GW))
                    repeat_feat[1]=np.ones((GH,GW))
                    repeat_feat[2]=np.zeros((GH,GW))
                    if pre_actions[-50:].count(pre_actions[-1]) == len(pre_actions[-50:]) and len(pre_actions[-50:])==50:
                        repeat_feat[0]=np.zeros((GH,GW))
                        repeat_feat[1]=np.zeros((GH,GW))
                        repeat_feat[2]=np.ones((GH,GW))

                


        if pre_locations:
            if pre_locations[-5:].count(pre_locations[-1]) == len(pre_locations[-5:]) and len(pre_locations[-5:])==5:
                repeat_feat[3]=np.ones((GH,GW))
                repeat_feat[4]=np.zeros((GH,GW))
                repeat_feat[5]=np.zeros((GH,GW))
                if pre_locations[-10:].count(pre_locations[-1]) == len(pre_locations[-10:]) and len(pre_locations[-10:])==10:
                    repeat_feat[3]=np.zeros((GH,GW))
                    repeat_feat[4]=np.ones((GH,GW))
                    repeat_feat[5]=np.zeros((GH,GW))
                    if pre_locations[-50:].count(pre_locations[-1]) == len(pre_locations[-50:]) and len(pre_locations[-50:])==50:
                        repeat_feat[3]=np.zeros((GH,GW))
                        repeat_feat[4]=np.zeros((GH,GW))
                        repeat_feat[5]=np.ones((GH,GW))

                
#         print(orientation_feat[0].shape)
        
        final_feat = np.stack((agentloc_feat,
                               visited_feat,
                               stench_feat,
                               breeze_feat,
                               orientation_feat[0],
                               orientation_feat[1],
                               orientation_feat[2],
                               orientation_feat[3],
                               hasgold_feat,
                               glitter_feat,
                               hasarrow_feat,
                               scream_feat,  
                               repeat_feat[0],
                               repeat_feat[1],
                              repeat_feat[2],
                              repeat_feat[3],
                              repeat_feat[4],
                              repeat_feat[5]
                              ),axis=2)
        return final_feat
        
        

    def initialize(self, GridWidth,GridHeight,pitProb,allowClimbWithoutGold):
        self.gridwidth = GridWidth
        self.gridheight = GridHeight 
        self.pitprob = pitProb
        self.allowclimbwithoutgold = allowClimbWithoutGold 
        coords_list = []
        pit_list = []
        for x in range(1,self.gridwidth,1):
            for y in range(1,self.gridheight,1):
                coords_list.append((x,y))
                rand_num = random.uniform(0, 1)
                if rand_num < self.pitprob:
                    pit_list.append((x,y))
        self.pitlocations = pit_list
        self.wumpuslocation = random.choice(coords_list)
        self.goldlocation = random.choice(coords_list)
#         self.goldlocation = (1,0)
        self.agent = AgentState(Coords = (0,0), Orientation = 'East', HasGold = False, HasArrow = True, IsAlive = True, WumpusAlive = True,
                 beelineActionList=[],
                 stenchLocations = [],
                 breezeLocations = [],
                 visitedLocations = [(0,0)],
                 previousActions = [],
                 previousLocations = [(0,0)],
                 repeatFeat = [0,0],
                 recentReward = 0,
                 totalReward = 0)
        self.agent.hasgold=False
        newEnv_class = self
        percept_class = Percept(newEnv_class.isStench(),
                                   newEnv_class.isBreeze(),
                                   False,
                                   False,
                                   False,
                                   False,
                                   0.0)
        return newEnv_class,percept_class
        
                























