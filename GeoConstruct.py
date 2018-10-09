import numpy as np
from B_n import *
#from scipy import special, optimize
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.lines as mlines


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
    #This is the number of hidden nodes
    height = 0;
    #This is the height of the prism box
    radius = 0;
    #This is the radius of Bn
    sourceAngle = 0
    #This is the phi angle
    hiddenNodeMotMatrix = None;
    #This is the motMatrix for the hidden Nodes
    hiddenNodeTstMatrix = None;
    #This is the timeMatrix for the hidden nodes
    hiddenNodeTijMatrix = None;
    #This is the time delay
    def __init__(self, numVertices, height, radius, sourceAngle):
        self.NumberOfVertices = numVertices;
        self.NumberOfPrism = 0;
        self.height = height;
        self.radius = radius;
        self.sourceAngle = sourceAngle;


    def initializeMatrices( self, MotMatrix, TstMatrix, WgtMatrix ):
        print("Initializing matrices");
        self.MotMatrix = MotMatrix;
        self.TstMatrix = TstMatrix;
        self.WgtMatrix = WgtMatrix;

    def initializeHNodeMatrix( self, hiddenNodeMot, hiddenNodeTstMatrix, hiddenNodeTijMatrix):
        self.hiddenNodeMotMatrix = hiddenNodeMot;
        self.hiddenNodeTstMatrix = hiddenNodeTstMatrix;
        self.hiddenNodeTijMatrix = hiddenNodeTijMatrix;

    def initializeFirstBn(self,ax):
        """
        This initializes the first Bn which has its norm vector
        parallel to the z axis
        """
        firstBn = B_n(self.NumberOfVertices,True,self.radius,(0,0,0),(0,0,1));
        firstBn.initializeFirst();
        firstBn.plotB_n(ax);
        firstBn.drawLines(ax);
        firstBn.printVertexCoordinate();


    def initializeBn(self,ax,normVec):
        Bn = B_n(self.NumberOfVertices,False,self.radius,(0,0,0), normVec);
        Bn.initializeSelf();
        Bn.dotProductVecSet();
        #Bn.plotVertex(ax,Bn.verticesSet[0]);
        Bn.plotCentroidAndNorm(ax);
        Bn.plotVertices(ax);
