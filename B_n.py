import numpy as np
import random
import math
from Vertex import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from scipy.optimize import fmin
from numpy import linalg as LA



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
    centroid = None;
    #This is the centroid of the Bn
    normalVector = None;
    #This is the plane for the Bn
    projectionVector = None;
    #This is the vector applies an affine transformation to the proection
    baseVector = None;
    #This is the vector from which to compare the projection vector
    verticesActivated = None;
    #Multiple vertices can be activated at a given time step
    isFirst= False;
    #This is the inductive case where you have to set the points for Bn
    isBottom = False;
    #Bn is either the top or the bottom
    #isTop = False;
    timeInstance = 0;
    #This is the time that Bn represents

    def __init__(self, numOfVertices, isFirst, radius, centroid, normVec, isBottom):
        self.numOfVertices = numOfVertices;
        self.isFirst = isFirst;
        self.radius = radius;
        self.centroid = centroid;
        self.verticesSet = [];
        self.normalVector = self.unitVec(normVec);
        self.isBottom = isBottom;

    def unitVec(self,vectorToUnit):
        amtToDivide =  LA.norm(vectorToUnit);
        vecUnit = [];
        for i in range(len(vectorToUnit)):
            vecUnit.append(vectorToUnit[i]/amtToDivide);
        return   vecUnit;

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
                self.verticesSet.append(vHolder);



    def initializeSelf(self):
        """
        This initializes Bn with the norm vec
        where none of the positions of the vertices are given
        """
        firstVpoint=self.getFirstPoint();
        v1= Vertex(self.numOfVertices,firstVpoint,1);
        self.verticesSet.append(v1);
        self.currentNumOfVertices+=1;
        self.generateVertices(self.verticesSet[0]);
        self.printVertexCoordinate();

    def plotVertices(self,ax):
        for x in range(self.numOfVertices):
            self.plotVertex(ax,self.verticesSet[x]);
        return

    def generateVertices(self, vertexStart):
        Beta =  2*np.pi/self.numOfVertices;
        currentVertex = vertexStart;
        for x in range(1,self.numOfVertices):
            #Iterates and then updates the next vertex to startfrom
            currentVertex = self.generateNextVertex(Beta,currentVertex);
            print("Creating Vertex "+ str(x+1));
        return;

    def dotProductVecSet(self):
        for x in range(self.numOfVertices):
            vecX = self.verticesSet[x].vertexPosition[0] - self.centroid[0];
            vecY = self.verticesSet[x].vertexPosition[1] - self.centroid[1];
            vecZ = self.verticesSet[x].vertexPosition[2] - self.centroid[2];
            vecArray = np.array([vecX,vecY,vecZ]);
            normArray = np.array(self.normalVector);
            result = np.absolute(np.dot(vecArray,normArray));
            print("dot result  ("+str(x+1)+") :"+str(result));
        return;

    def generateNextVertex(self,Beta, currentVertex):
        """
        Need to put the edge case for n=4
        where Beta >=90
        """
        vecX = currentVertex.vertexPosition[0] - self.centroid[0];
        vecY = currentVertex.vertexPosition[1] - self.centroid[1];
        vecZ = currentVertex.vertexPosition[2] - self.centroid[2];
        VtoCen = [vecX,vecY,vecZ];
        Vheight = np.cross(VtoCen,self.normalVector);
        self.scaleVector(Vheight,self.radius*np.tan(Beta))
        newVec = VtoCen+Vheight;
        self.scaleVector(newVec,self.radius);
        pointX = self.centroid[0] + newVec[0];
        pointY = self.centroid[1] + newVec[1];
        pointZ = self.centroid[2] + newVec[2];
        pointVnew =(pointX, pointY, pointZ);
        self.currentNumOfVertices+=1;
        vertexNew = Vertex(self.numOfVertices,pointVnew,self.currentNumOfVertices);
        self.verticesSet.append(vertexNew);
        return vertexNew;

    def generateProjBn(self,height,projVec,baseVec):
        translateVec =[0,0,0];
        newCentroid = [0,0,0];
        print("Normal Vector: "+str(self.normalVector));
        print("Base Vector: "+str(baseVec));
        if self.checkIfVecEqual(baseVec,self.normalVector) ==  False:
            for y in range(3):
                print("y: "+str(y));
                translateVec[y] = self.normalVector[y] - baseVec[y];
        else:
            translateVec = self.normalVector;
        for z in range(3):
            newCentroid[z] = self.centroid[z] +translateVec[z];
        newCentroid = tuple(newCentroid);
        BnNew = B_n(self.numOfVertices,False,self.radius,newCentroid,self.normalVector,False);
        #This represent the top
        self.scaleVector(translateVec,height);
        iteratedTuple = [0,0,0];
        for x in range(self.numOfVertices):
            iteratedTuple[0] = self.verticesSet[x].vertexPosition[0]+ translateVec[0];
            iteratedTuple[1] = self.verticesSet[x].vertexPosition[1]+ translateVec[1];
            iteratedTuple[2] = self.verticesSet[x].vertexPosition[2]+ translateVec[2];
            vertexNew = Vertex(self.numOfVertices,tuple(iteratedTuple),x+1);
            BnNew.verticesSet.append(vertexNew);
        return BnNew;

    def getVertex(self, vertexID):
        vertexTemp = None;
        for x in range(self.numOfVertices):
            vertexTemp = self.verticesSet[x];
            if vertexTemp.vertexID == vertexID:
                return vertexTemp;
        print(" Get vertex function doesn't work")
        return 0;

    def scaleVector(self, vectorScale, size):
        print("Scale size: "+ str(size));
        print("Vector to scale: "+str(vectorScale));
        alpha = size/LA.norm(vectorScale);
        vectorScale[0]=alpha*vectorScale[0];
        vectorScale[1]=alpha*vectorScale[1];
        vectorScale[2]=alpha*vectorScale[2];
        return;
    def dotPwithNorm(self, t):
        """
        (x-c1)^2 + (z-c3)^2 = R is equation for circle
        """

        xComp=self.radius*np.cos(t);
        zComp=self.radius*np.sin(t);
        compArray = np.array([xComp,0,zComp]);
        normArray = np.array(self.normalVector);
        result = np.absolute(np.dot(compArray,normArray));
        #result = np.dot(compArray,normArray);
        #print( "Result of Dot Product: "+ str(result));
        return result;

    def checkIfVecEqual(self, vec1, vec2):
        for x in range(3):
            if vec1[x] != vec2[x]:
                return False;
        return True;



    def getFirstPoint(self):
        """
        Algorithm 1.2.1
        To get the first vertex, fix the y axis
        Iterate around the circle until the dot
        product with n is 0. There are 2 points for
        this.

        (x-c1)^2 + (z-c3)^2 = R is equation for circle
        n1(x-c1) + n2(y-c2) + n3(z-c3) =0 is equation for plane
        """

        minimum = fmin(self.dotPwithNorm,0);
        xPoint = self.centroid[0] + self.radius*np.cos(minimum[0]);
        yPoint = self.centroid[1];
        zPoint = self.centroid[2] + self.radius*np.sin(minimum[0]);
        print(" Point: "+str(xPoint)+", "+str(yPoint)+ ", "+str(zPoint)+")");
        vecTempX = self.radius*np.cos(minimum[0]);
        vecTempY = 0;
        vecTempZz = self.radius*np.sin(minimum[0]);
        normArray = np.array(self.normalVector);
        compArray = np.array([vecTempX,vecTempY,vecTempZz]);
        print(" Dot Prod of First "+str(np.dot(normArray,compArray)));
        return (xPoint,yPoint,zPoint);


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


    def plotCentroidAndNorm(self,ax):
        endX = self.centroid[0]+self.normalVector[0];
        endY = self.centroid[1]+self.normalVector[1];
        endZ = self.centroid[2]+self.normalVector[2];
        ax.scatter(self.centroid[0],self.centroid[1],self.centroid[2], c = 'r');
        ax.scatter(endX, endY, endZ);
        newPoint = [endX, endY, endZ];
        ax.plot([self.centroid[0],endX],[self.centroid[1],endY],[self.centroid[2],endZ]);


    def plotVertex(self, ax, vertex):
        xPos = vertex.vertexPosition[0];
        yPos = vertex.vertexPosition[1];
        zPos = vertex.vertexPosition[2];
        ax.scatter(xPos,yPos,zPos,c = 'r');


    def drawLineToConnectBn(self,ax,Bn):
        for x in range(self.numOfVertices):
            vertex1 = np.array(self.verticesSet[x].vertexPosition);
            vertex2 = np.array(Bn.verticesSet[x].vertexPosition);
            v1Name = self.verticesSet[x].vertexID;
            v2Name = self.verticesSet[x].vertexID;
            print("Drawing line for "+ str(v1Name)+" , "+str(v2Name));
            ax.plot([vertex1[0],vertex2[0]],[vertex1[1],vertex2[1]],[vertex1[2],vertex2[2]]);

    def drawLines(self,ax):
        for i in range(0,self.numOfVertices-1):
                vertex1 = np.array(self.verticesSet[i].vertexPosition);
                vertex2 = np.array(self.verticesSet[i+1].vertexPosition);
                v1Name = self.verticesSet[i].vertexID;
                v2Name = self.verticesSet[i+1].vertexID;
                print("Drawing line for "+ str(v1Name)+" , "+str(v2Name));
                ax.plot([vertex1[0],vertex2[0]],[vertex1[1],vertex2[1]],[vertex1[2],vertex2[2]]);
        vertex1 = np.array(self.verticesSet[0].vertexPosition);
        vertex2 = np.array(self.verticesSet[self.numOfVertices-1].vertexPosition);
        v1Name = self.verticesSet[0].vertexID;
        v2Name = self.verticesSet[self.numOfVertices-1].vertexID;
        print("Drawing line for "+ str(v1Name)+" , "+str(v2Name));
        print(" v1 position: "+str(self.verticesSet[0].vertexPosition));
        print(" v12 position: :"+str(self.verticesSet[self.numOfVertices-1].vertexPosition));
        print(" v1 shape: "+str(vertex1.shape));
        print(" v2 shape: "+str(vertex2.shape));
        ax.plot([vertex1[0],vertex2[0]],[vertex1[1],vertex2[1]],[vertex1[2],vertex2[2]]);


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
