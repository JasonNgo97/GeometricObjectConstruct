from VertexState import *

class NetworkState:
    nState = None;
    #This is the list of vertices states
    numOfVertices = 0;
    #This is the number of vertices
    indexBegin = 0;
    #index to begin analysis
    timeBegin = 0;
    #corresponding time
    indexEnd = 0;
    #index to end analysis
    timeEnd = 0;
    #corresponding time
    timeVec = None;
    #This is the vec with time for indexing
    hNodeMot = None;
    #This is the Mot with the hNodes
    TijMatrix = None;
    #This is the matrix with time delays
    WijMatrix = None;
    #This is the matrix with the weights
    activationThreshold = None;
    #This is the activation threshold
    nStateList = None;
    #This holds the list of nState
    indexIter = 0;

    def __init__ (self, numV, indexBegin, timeVec, indexEnd, hNodeMot, TijMatrix, WijMatrix):
        self.numOfVertices = numV;
        self.indexBegin = indexBegin;
        self.indexEnd = indexEnd;
        self.timeVec = timeVec;
        self.timeBegin = timeVec[indexBegin];
        self.timeEnd = timeVec[indexEnd];
        self.hNodeMot = hNodeMot;
        self.TijMatrix = TijMatrix;
        self.WijMatrix = WijMatrix;
        self.activationThreshold = 4;
        self.nState = [];
        self.nStateList = [];
        self.indexIter = 0;
        return;

    def initNetwork(self):
        print("In init network");
        if self.noInputNodeActivations(self.indexBegin,self.indexEnd) == False:
            return False;
        print("Begin Time "+str(self.timeBegin));
        for i in range(self.numOfVertices):
            vState = VertexState(i+1,self.numOfVertices,self.activationThreshold,self.indexBegin, self.indexEnd, self.hNodeMot,self.timeVec, self.TijMatrix, self.WijMatrix);
            ableToInit = vState.initState();
            #This is the error condition
            if ableToInit == False:
                print("Unable to init");
                return False;
            self.nState.append(vState);
        print("Able to init");
        print("");
        self.printState();
        print("");
        self.indexIter = self.indexIter +1;
        return True;

    def updateNetwork(self, indexCurrent, vAindex):
        """
        Given the vertex that actives and a current index
        this function updates the network accordingly
        """
        listSignal =[];
        #Iterate through the elements
        for i in range(self.numOfVertices):
            elem = self.nState[i];
            if elem.vertexID != (vAindex+1) :
                ableToInit= elem.updateState(indexCurrent, vAindex);
                if ableToInit:
                    listSignal.append(elem);
        return listSignal;



    def determineStateInterval(self, indexBegin, indexEnd):
        if indexBegin != self.indexBegin:
            print("Invalid Begin Index");
            return False;
        self.initNetwork();
        indexIter = self.getNextTimeIndex(self.indexBegin);

        """
        Iterate through the indices
        """
        while(indexIter < indexEnd):
            print("Time :"+str(self.timeVec[indexIter]));
            listCurrSigNetwork = [];
            listAV = self.determineActiveVertices(indexIter);
            #print("AV size: " + str(len(listAV)));
            """
            This is the case for output nodes
            """
            if len(listAV) == 0:
                self.setNetworkTime(self.timeVec[indexIter],indexIter);
            """
            Iterate through activated vertices
            """
            for x in range(len(listAV)):
                print("Activated Vertex: "+str(listAV[x]));
                listToAdd = self.updateNetwork(indexIter,listAV[x]-1);
                elem = (listAV[x], listToAdd);
                listCurrSigNetwork.append(elem);
            """
            Update index and print the state
            """
            print("");
            self.printState();
            print("");
            self.indexIter = self.indexIter +1;
            indexIter = self.getNextTimeIndex(indexIter);
            self.nStateList.append(listCurrSigNetwork);
        return True;



#These are helper functions
    def determineActiveVertices(self, currentIndex):
        listAV = [];
        for x in range(self.numOfVertices):
            if(self.hNodeMot[x][currentIndex] != 0):
                listAV.append(x+1);
        return listAV;


    def setNetworkTime(self, time,index):
        for x in range(self.numOfVertices):

            elem = self.nState[x];
            elem.indexCurr = index;
            elem.timeCurr = time;
        return;

    def getNextTimeIndex(self, currentIndex):

        indexIter = currentIndex;
        currTime = self.timeVec[indexIter];
        while self.timeVec[indexIter] == currTime:
            indexIter = indexIter +1;
        timeReturn = self.timeVec[indexIter];
        print("Curr Time: " + str(currTime));
        print("Found Time: " + str(timeReturn));
        return indexIter;


    def printState(self):
        print(" INDEX: "+str(self.indexIter));
        print("-------------------------------------");
        for i in range(self.numOfVertices):
            #print(str(i+1));
            self.nState[i].printState();
        print("-------------------------------------");
        return;

    def noInputNodeActivations(self, indexBegin, indexEnd):
        #print("Inside InputNode");
        for i in range(indexBegin,indexEnd):
            for j in range(self.numOfVertices):
                if self.hNodeMot[j][i] == -1 :
                    print("Input Node at ["+str(j)+"]["+str(i)+"]");
                    print("Time "+str(self.timeVec[i]));
                    return False
        return True
