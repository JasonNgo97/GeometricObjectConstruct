import numpy as np
import random
import math
from Vertex import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.lines as mlines




class B_n:
    """This class is used for top and bottom of the prism"""


    verticesSet = None;
    #This is an ordered set that hold the vertices and its points
    #Each Bn has its own set of vertices
    numOfVertices = 0;
    #This is the number of vertices in the hidden node
    currentNumOfVertices = 0;
    #This jsut holds the num of vertices in construction
    radius = 0;
    #This is the radius of the n-gon
    Centroid = None;
    #This is the centroid of the Bn
    NormalVector = None;
    #This is the plane for the Bn
    verticesActivated = None;
    #Multiple vertices can be activated at a given time step
    isFirst = False;
    #This is the inductive case where you have to set the points for Bn
    isBottom = False;
    #Bn is either the top or the bottom
    timeInstance = 0;
    #This is the time that Bn represents

    def __init__(self, numOfVertices, isFirst, radius, centroid):
        self.numOfVertices = numOfVertices;
        self.isFirst = isFirst;
        self.radius = radius;
        self.Centroid = centroid;
        self.verticesSet = [];


    def initializeFirst(self):
        alpha = 2*np.pi/self.numOfVertices;

        if self.isFirst == False:
            return
        else:
            centroid = (0,0,0)
            #Always start at the origin
            v1 = Vertex(self.numOfVertices, (self.radius,0 ,0), 1);
            self.verticesSet.append(v1);
            xPos = 0;
            yPos = 0;
            vHolder = None;
            for i in range(1, self.numOfVertices):
                xPos = self.radius * np.cos(i*alpha);
                yPos = self.radius * np.sin(i*alpha);
                vHolder = Vertex(self.numOfVertices,(xPos, yPos, 0),i+1);
                self.verticesSet.append(vHolder)

    def printVertexCoordinate(self):
        print(" Printing Vertex Coordinates");
        for i in range(self.numOfVertices):
            self.verticesSet[i].printContents();
        print(" Printing out edge distances");
        vertex1 = None;
        vertex2 = None;
        dist = 0;
        for i in range(0,self.numOfVertices-1):
            vertex1 = np.array(self.verticesSet[i].vertexPosition);
            vertex2 = np.array(self.verticesSet[i+1].vertexPosition);
            dist = self.distanceBetweenPoints(vertex1,vertex2);
            print(str(i)+","+str(i+1)+": "+str(dist));

    def drawLines(self,ax):
        for i in range(0,self.numOfVertices-1):
                vertex1 = np.array(self.verticesSet[i].vertexPosition);
                vertex2 = np.array(self.verticesSet[i+1].vertexPosition);
                v1Name = self.verticesSet[i].vertexID;
                v2Name = self.verticesSet[i+1].vertexID;
                print("Drawing line for "+ str(v1Name)+" , "+str(v2Name));
                ax.plot([vertex1[0],vertex2[0]],[vertex1[1],vertex2[1]],[0,0]);

    def plotB_n(self, ax):
        xPos = 0;
        yPos = 0;
        zPos = 0;
        for i in range(self.numOfVertices):
            xPos = self.verticesSet[i].vertexPosition[0];
            yPos = self.verticesSet[i].vertexPosition[1];
            zPos = self.verticesSet[i].vertexPosition[2];
            ax.scatter(xPos,yPos,zPos,c = 'r');
        ax.set_xlabel('X Label');
        ax.set_ylabel('Y Label');
        ax.set_zlabel('Z Label');

    def distanceBetweenPoints(self, point1, point2):
        return np.linalg.norm(point1 - point2);
