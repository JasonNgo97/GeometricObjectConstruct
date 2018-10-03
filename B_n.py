import numpy as np
import random
import math




class B_n:
    """This class is used for top and bottom of the prism"""


    verticesSet = None;
    #This is an ordered set that hold the vertices and its points
    #Each Bn has its own set of vertices
    numOfVertices = 0;
    #This is the number of vertices in the hidden node
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
