

class VertexState:

        isActive = False;
        #This is if the vertex is currently active
        vertexID = 0;
        #This is the vertex's identity
        numOfVertices = 0;
        #This is number of hidden nodes
        indexA = 0;
        #Index of activation
        timeA = 0;
        #Time of activation
        indexLA = 0;
        #This is the last index of activation
        timeLA = 0;
        #This is the time of last activation
        indexCurr = 0;
        #This is the index we are currently looking at
        timeCurr = 0;
        #This is the current time
        indexNA = 0;
        #This is the index of next activation
        timeNA = 0;
        #This is the time of next activation
        indexBegin = 0;
        #This is the beginning index for analysis
        timeBegin = 0;
        #This is the corresponding time for indexBegin
        indexEnd = 0;
        #This is the end index for analysis
        timeEnd = 0;
        #This is the corresponding time
        aN = 0;
        #This is the activation number
        cT = 0;
        #This is the current threshold
        vCList = None;
        #This is a list of the contributing vertices form of (vC, wC)
        prismLA = None;
        #This is the prism corresponding to the last activation
        vCauseActivate = 0;
        #This is the vID  that caused this vertex's activation
        hNodeMot = None;
        #This is the Mot for hNodes
        timeVec = None;
        #This holds the time vector and index for Mot
        TijMatrix = None;
        #This is the time delay matrix
        WijMatrix = None;
        #This is the weight matrix

        def __init__(self, vID, numV, aN, indexBegin, indexEnd, HNodeMot, timeVec, TijMatrix, WijMatrix):
            self.vertexID = vID;
            self.numOfVertices = numV;
            self.aN = aN;
            self.indexBegin = indexBegin;
            self.indexEnd = indexEnd;
            self.hNodeMot = HNodeMot;
            self.timeVec = timeVec;
            self.TijMatrix = TijMatrix;
            self.WijMatrix = WijMatrix;
            return
