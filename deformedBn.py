import numpy
class deformedBn:
    """"
    This class is used to deform the line segments according
    to the time delays and weights
    """"
    BnTop = None;
    #This is the Bn containing the points to translate
    BnBottom = None;
    #This is the Bn containing the activated vertex
    VertexActivated = None;
    #This is the vertex activated
    VerticesSignaled = None;
    #These are the vertices signaled hence the points to deform
    OriginalLineSet = None;
    #This is the line set
    DeformedLineSet = None;
    #This is the deformed DeformedLineSet
    ComputedResultantVector = None;
    #This is the resultant vector calculated from deformed  Bn
