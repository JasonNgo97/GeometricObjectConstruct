import numpy
import math
import GeometricObjectConstruct.B_n
import GeometricObjectConstruct.Vertex


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
    index = 0;
    #This is the index of the prism in the time sequence
    OriginalLineSet = None;
    #This is the original line set from the projection
    DeformedLineSet = None;
    #This is the line set deformed according to the time delays
    NormalVectorBottom = None;
    #This is the normal vector from bottom
    ResultantNormVectorTop = None;
    #This is the resultant vector calculated from the deformed line set
