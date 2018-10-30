import numpy as np
from Vertex import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from scipy.optimize import fmin
from numpy import linalg as LA
class deformedBn:
    """"
    This class is used to deform the line segments according
    to the time delays and weights
    """"
    numOfSignaledVert = 0;
    signaledVertexSet = None;
    nextVertexActivated = None;
    newNorm = None;
    centroidOfDeformed = None;
    radius = None;
    vertSource = None;

    def __init__(self, numOfSignaledVert, radius, lineSet, vertSource):
        self.numOfSignaledVert = numOfSignaledVert;
        self.radius = radius;
        self.signaledVertexSet = [];
        self.vertSource = vertSource;
        initializeSignalVert(lineSet);
        self.newNorm = [1,2,4];
        #This is just a hard code test case
        pass;



    def initializeSignalVert(self, lineSet):
        tempLine = None;
        vertToAdd = None;
        for x in range(len(lineSet)):
            tempLine = lineSet[x];
            vertToAdd = tempLine.newVertexSignaled;
            self.signaledVertexSet.append(vertToAdd);
        return;


    def getDistances(self, BnOther):
        dist = 0;
        pointTemp1 = None;
        pointTemp2 = None;
        vertexTemp = None;
        vertexComp = None;
        for x in range(self.numOfSignaledVert):
            vertexTemp = signaledVertexSet[x];
            vertexComp = BnOther.getVertex(vertexTemp.vertexID);
            pointTemp1 = np.array(vertexTemp.vertexPosition);
            pointTemp2 = np.array(vertexComp.vertexPosition);
            dist += np.linalg.norm(pointTemp1 - pointTemp2);
        return dist;
