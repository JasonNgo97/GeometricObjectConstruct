import numpy
import math

class Vertex:

    vertexID = 0;
    #This is its index as a hidden Node
    hiddenNodeOffset = 0;
    #This is a constant used to index the matrix
    totalNumHNodes = 0;
    #This is the total number of hidden nodes
    vertexPosition = None;
    #This is its position in Bn
    isActivated = False;
    #This determines if the node is activated at this instance
    isSignaled = False;
    #If this vertex is signaled
    sourceNodeForSignal = None;
    #If this node is receives signal at this instance,  here is the source
    nodeSignalsReceived = None;
    #If it is not activated, these are signals it received
    activationThreshold = 0;
    #This is the activation threshold. Is constant through GeoConstuct
    remainingThreshold = 0;
    #Amount needed to activate
    timeInstance = 0;
    #The time value currently
    timeIndex = 0;
    #The first time index in Mot file
