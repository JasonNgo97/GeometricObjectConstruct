import numpy
class GeoConstruct:
    PrismSequence = None;
    #This holds our prism sequence
    NumberOfPrism = 0;
    #This is the number of prisms in the time sequence
    MotMatrix = None;
    #This contains the time sequence we are analyzing
    TstMatrix = None;
    #This is the time source node matrix
    WgtMatrix = None;
    #This is the weight matrix for the edges
    TijMatrix = None;
    #This is the time delay matrix
    beginSteadyState = 0;
    #This is the index for steady state
    endSteadyState = 0;
    #This is the index for the end of steady state
    NumberOfVertices = 0;
    #This is the number of vertices in the network
    def _init_(self):
        
