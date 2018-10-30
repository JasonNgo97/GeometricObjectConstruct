import numpy as np
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
    BnDeformed = None;
    #This is the Bn that is deformed
    vertexActivated= None;
    #The prism contains a single vertec activated
    verticesSignaled = None;
    #These are the vertices signaled
    numOfVertices = None;
    #The number of vertices
    index = 0;
    #This is the index of the prism in the time sequence
    lineSet = None;
    #This is the original line set from the projection
    #DeformedLineSet = None;
    #This is the line set deformed according to the time delays
    NormalVector = None;
    #This holds the normal vector for the bottom and top initialially before deformation
    NormalVectorBottom = None;
    #This is the normal vector for the bottom
    radius = None;
    #This is the radius for Bn
    NormalVectorTop = None;
    #This is the normal vector from bottom
    ResultantNormVectorTop = None;
    #This is from the deformed Bn
    firstCentroid = None;

    tempVertActivateNext = None;

    BnNext = None;

    #This is the resultant vector calculated from the deformed line set
    def __init__(self, numOfVertices, BnBottom, height, normVec, projVec, baseVec):
        self.BnBottom = BnBottom;
        self.height = height;
        self.numOfVertices = numOfVertices;
        self.NormalVectorBottom = normVec;
        self.NormalVector = normVec;
        self.BnTop = BnBottom.generateProjBn(self.height,projVec, baseVec);
        self.lineSet = [];
        self.radius= BnBottom.radius;

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
            self.lineSet.append(tempLine);

    def deformLines(self):
        """
        This is a function to be implemented later
        """
        pass;

    def drawTopBottomBn(self,ax):
        self.BnTop.plotVertices(ax);
        self.BnTop.drawLines(ax);
        self.BnBottom.plotVertices(ax);
        self.BnBottom.drawLines(ax);
        return;

    def drawNewBn(self,ax):
        self.BnNext.plotVertices(ax);
        return;

    def drawLines(self,ax):
        tempLine = None;
        for x in range(len(self.lineSet)):
            tempLine = self.lineSet[x];
            tempLine.drawLine(ax);
            tempLine.drawDefLine(ax);
        return;

    def initializeDeformedBn(self):
        """
        Need to account for edge case when lineSet is empty
        """
        numOfSignaledVert = len(lineSet);
        radius = self.BnBottom.radius;
        vertSource = lineSet[0].vertexSource;
        self.BnDeformed = deformedBn(lineSet,numOfSignaledVert, radius, vertSource);


    def BnFitDist(self, vActivateNext):
        """
        This iterates and finds the minimum distance
        """
        self.getFirstCentroid(vActivateNext);
        self.tempVertActivateNext= vActivateNext;
        minT = fmin(self.BnIter, 0);
        tMin = minT[0];
        centroidMin = self.getCentroid(tMin);
        BnNew = B_n(self.numOfVertices,False, self.radius, centroidMin,self.ResultantNormVectorTop,True);
        self.BnNext = BnNew;
        return BnNew;


    def BnIter(self,t):
        """
        Given a vertex and parameter t, this computes the distance
        In the end you want to find the minimum t
        """
        radius = self.radius;
        normVecNew = self.BnDeformed.newNorm;
        self.ResultantNormVectorTop = normVecNew;
        centroidTemp = getCentroid(t,radius);
        BnTemp = Bn(self.numOfVertices,False,radius,centroidTemp, normVecNew, False);
        BnTemp.initializeSelf(vActivateNext);
        distTemp = self.BnDeformed.getDistances(BnTemp);
        return distTemp;

    def dotPwithNorm(self, t):
        """
        (x-c1)^2 + (z-c3)^2 = R is equation for circle
        """
        xComp=self.radius*np.cos(t);
        zComp=self.radius*np.sin(t);
        compArray = np.array([xComp,0,zComp]);
        normArray = np.array(ResultantNormVectorTop);
        result = np.absolute(np.dot(compArray,normArray));
        #result = np.dot(compArray,normArray);
        #print( "Result of Dot Product: "+ str(result));
        return result;

    def getFirstCentroid(self, vActivateNext):
        """
        This initializes the first centroid on the circle
        """
        minimum = fmin(self,dotPwithNorm,0);
        xPoint = vActivateNext.vertexPosition[0] + self.radius*np.cos(minimum[0]);
        yPoint = vActivateNext.centroid[1];
        zPoint = vActivateNext.centroid[2] + self.radius*np.sin(minimum[0]);
        self.firstCentroid = [xPoint,yPoint,zPoint];
        return;


    def getCentroid(self, t):
        """
        So pretty much, this is the function that finds the position
        of the centroid
        """
        vecO = self.generateVecFrom2pts(self.firstCentroid, list(self.tempVertActivateNext.vertexPosition));
        vecG = np.cross(vecO,self.ResultantNormVectorTop);
        self.scaleVector(vecG,self.radius*np.tan(t));
        newVec = vecO + vecG;
        verPos = list(self.tempVertActivateNext.vertexPosition);
        centroidPoint = newVec+ verPos;
        return centroidPoint;


    def generateVecFrom2pts(self, pointS, pointD):
        vecToReturn = pointD - pointS;
        return vecToReturn;

    def scaleVector(self, vectorScale, size):
        print("Scale size: "+ str(size));
        print("Vector to scale: "+str(vectorScale));
        alpha = size/LA.norm(vectorScale);
        vectorScale[0]=alpha*vectorScale[0];
        vectorScale[1]=alpha*vectorScale[1];
        vectorScale[2]=alpha*vectorScale[2];
        return;

    def printLineInfo(self):
        for x in range(len(self.lineSet)):
            self.lineSet[x].scaleLine(10-x+1);
