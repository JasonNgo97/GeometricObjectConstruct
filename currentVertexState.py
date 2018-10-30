import numpy as np
from GeoConstuct import *



class currentVertexState:
    """
    These are the member variables
    """
    vertexID = None;
    #This is the ID of the hNode
    activationThreshold = 0;
    #This is the maximum threshold to activate node
    currentThreshold = 0;
    #This is the current threshold  needed to activate the node
    timeIndex = 0;
    #This holds the time index that we are looking at
    currentTime = 0;
    #This is the time that we are looking at
    verticesSignaled = None;
    #These are the vertices that it has signaled
    #I think it is going to be used later
    verticesCA = None;
    #These are the vertices contributing to next activation
    prismLA = None;
    #This is the prism corresponding to its last activation
    timeDelayCA = None;
    #These are the time delays corresponding to the vCA
    isActivated = False;
    #This tells you if the node is activated at current time
    indexLA = 0;
    #This is the index corresponding to the last activation
    indexNA = 0;
    #This is the index corresponding to next activation
    hNodeMotMatrix = None;
    #This is the Mot Matrix
    numOfVertices = 0;
    #This is number of vertices in the network
    lengthOfSequence = 0;


def __init__(self, vertexID, activationNumber, hNodeMotMatrix):
    self.vertexID = vertexID;
    self.activationThreshold = activationNumber;
    self.hNodeMotMatrix = hNodeMotMatrix;
    tempTuple = np.array(self.hNodeMotMatrix).shape;
    self.numOfVertices = tempTuple[0];
    self.lengthOfSequence = tempTuple[1];
    return;



"""
This tells you if this is a valid index for steady state
which means no hiddenNodes
"""
def notInSS(self, timeIndex):
    for x in range(timeIndex, self.lengthOfSequence):
        #There is an input node
        if self.hNodeMotMatrix[vertexID-1][x] == -1:
            return False;
    return True;


"""
This tells you if the node is currently active
"""
def currentActive(self, timeIndex):
    if self.hNodeMotMatrix[timeIndex] != 0:
            return True;
    return False;

"""
This get the index of last activation
"""
def getLA(self, index):
    for x in range(index):
        if self.hNodeMotMatrix[self.vertexID][index - x] :
            return index-x;

"""
This is suppose to give the index
corresponding to the beginning
With the current activation, you slide it until the end
"""
def alignIndex(self, index):
        for x in range(index):
            if self.hNodeMotMatrix[self.vertexID-1][index-x] == 0:
                return index-x+1;
        print("This line is not supposed to execute");
        return -1;

"""
This aligns the index to the right
"""


"""
This gives you the index of last activation
"""
def getLA(self, vertID, indexStart):
    for x in range(indexStart):
        if self.hNodeMotMatrix[vertID -1][indexStart -x] != 0:
            return (indexStart -x);
    print("This is not supposed to execute here");
    return -1;


def getNA(self, vertID, indexStart):
    pass

"""
This function initializes the state given that
it is in a valid index. It returns true, if able
to initialize. Other wise, returns false
"""
def updateInitialState(self, timeIndex):

    indexStart = timeIndex;
    #Not a valid index for steady state
    if notInSS(timeIndex):
        return False;
    #This node is activated at this timeIndex
    #We make sure it starts at 0
    if currentActive(index):
        indexStart = alignIndex(indexStart);
        indexStart =indexStart-1;


    self.indexLA = getLA(vertexID, indexStart);
    self.indexLA = alignIndex(self.indexLA);
