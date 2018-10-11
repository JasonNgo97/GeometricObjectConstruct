import numpy
import math
from B_n import *
from Vertex import *
from Line import *


class Prism:
    """
    This class contains at least 2 Bn for the top and bottomself.
    There is 1 vertex that is activated.
    There is a set of vertices that it successfully signals
    """

    height = 0;
    #This is the height of the projection box
    BnTop = None;
    #This is the Bn on top which is the projected vertices
    BnBottom = None;
    #This is the Bn where a vertex is activated
    vertexActivated= None;
    #The prism contains a single vertec activated
    verticesSignaled = None;
    #These are the vertices signaled
    numOfVertices = None;
    #The number of vertices
    index = 0;
    #This is the index of the prism in the time sequence
    OriginalLineSet = None;
    #This is the original line set from the projection
    DeformedLineSet = None;
    #This is the line set deformed according to the time delays
    NormalVector = None;
    #This holds the normal vector for the bottom and top initialially before deformation
    NormalVectorBottom = None;
    #This holds the normal vector for the bottom
    NormalVectorTop = None;
    #This is the normal vector from bottom
    ResultantNormVectorTop = None;
    #This is the resultant vector calculated from the deformed line set
    def __init__(self, numOfVertices, BnBottom, height, normVec, projVec, baseVec):
        self.BnBottom = BnBottom;
        self.height = height;
        self.numOfVertices = numOfVertices;
        self.NormalVectorBottom = normVec;
        self.NormalVector = normVec;
        self.BnTop = BnBottom.generateProjBn(self.height,projVec, baseVec);
        self.OriginalLineSet = [];
        self.DeformedLineSet = [];

    def activatedVertex( self, vAiD, vSiD):
        #These take in strings
        verSignal = np.array(vSiD);
        signalSize = len(vSiD);
        vertexActivated = self.BnBottom.getVertex(vAiD);
        vertexTemp = None;
        tempLine = None;
        for x in range (signalSize):
            vertexTemp = self.BnTop.getVertex(vSiD[x]);
            tempLine = Line(vertexActivated,vertexTemp);
            self.OriginalLineSet.append(tempLine);

    def drawTopBottomBn(self,ax):
        self.BnTop.plotVertices(ax);
        self.BnTop.drawLines(ax);
        self.BnBottom.plotVertices(ax);
        self.BnBottom.drawLines(ax);
        return;

    def drawOLines(self,ax):
        tempLine = None;
        for x in range(len(self.OriginalLineSet)):
            tempLine = self.OriginalLineSet[x];
            tempLine.drawLine(ax);
        return;
