from VertexState import *

class NetworkState:
    nState = None;
    #This is the list of vertices states
    numOfVertices = 0;
    #This is the number of vertices
    indexBegin = 0;
    #index to begin analysis
    timeBegin = 0;
    #corresponding time
    indexEnd = 0;
    #index to end analysis
    timeEnd = 0;
    #corresponding time
    timeVec = None;
    #This is the vec with time for indexing
    hNodeMot = None;
    #This is the Mot with the hNodes
    TijMatrix = None;
    #This is the matrix with time delays
    WijMatrix = None;
    #This is the matrix with the weights

def __init__ (self, numV, indexBegin, timeVec, indexEnd, hNodeMot, TijMatrix, WijMatrix):
    self.numOfVertices = numV;
    self.indexBegin = indexBegin;
    self.indexEnd = indexEnd;
    self.timeVec = timeVec;
    self.timeBegin = timeVec[indexBegin];
    self.timeEnd = timeVec[indexEnd];
