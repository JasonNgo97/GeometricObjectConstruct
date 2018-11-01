

class VertexState:

    isActive = False;
    #This is if the vertex is currently active
    vertexID = 0;
    #This is the vertex's identity
    vIndex = 0;
    #This is the index within the network state
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
    rP = 0;
    #This is the refractory period
    vCList = None;
    #This is a list of the contributing vertices form of (vC, t, wC)
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
        self.vIndex = self.vertexID-1;
        self.numOfVertices = numV;
        self.aN = aN;
        #self.cT = aN;
        self.indexBegin = indexBegin;
        self.indexEnd = indexEnd;
        self.hNodeMot = HNodeMot;
        self.timeVec = timeVec;
        self.TijMatrix = TijMatrix;
        self.WijMatrix = WijMatrix;
        self.timeBegin = self.timeVec[indexBegin];
        self.timeEnd = self.timeVec[indexEnd];
        self.vCList = [];
        self.rP = 0.5 ** 6;
        #print("");
        #print("Weight Matrix");
        #print(str(WijMatrix));
        #print("");
        return


#These are the main methods
    def updateState(self, indexCurrent, vAindex):


        #print("Time Current&&&&&&&&&&&&&&: "+str(self.timeCurr));

        """
        Given a particular index and vertex that
        is active, this updates the state of the vertex.
        If it is able to signal, return true
        Otherwise return false.
        """
        if self.hNodeMot[vAindex][indexCurrent] == 0 :
            print("This vertex is not active.");
            return False;

        """
        Here we check if it is the next time.
        """
        timeToCheck = self.timeVec[indexCurrent];
        #print("Current threshold: "+str(self.cT));
        if self.checkIfNextTime(timeToCheck)== False:
            print("This is not the next time");
            return False;

        self.timeCurr = self.timeVec[indexCurrent];
        self.indexCurr = indexCurrent;
        timeToReach = self.timeCurr + self.TijMatrix[vAindex][self.vIndex];
        """
        If it is currently active
        """
        if self.isActive:
            print(str(self.vertexID) +" is currently Active");
            print("Time A:" + str(self.timeA));
            if vAindex == self.vIndex:
                print("This is itself");
                return True;
            elif timeToReach < self.timeA + self.rP:
                print("Unable to signal");
                return False;
            #This means it is able to signal
            #More specifically, it is the first node.
            else:
                print(" First Vertex to signal " + str(self.vertexID));
                print(" Time A:" + str(self.timeA));
                print(" Time Done Refract:" + str(self.timeA+self.rP) +". Time Reach: "+str(timeToReach));
                self.isActive = False;
                self.timeLA = self.timeA;
                self.cT = self.aN;
                self.vCList.clear();
                self.updateVertex(self.timeCurr,vAindex);

        #This means that it is not currently active
        else:
            self.updateVertex(self.timeCurr,vAindex);



        """
        This means that vA activated this vertex
        """
        if self.cT <= 0:
                print( str(vAindex+1) + " activated " + str(self.vertexID));
                self.isActive = True;
                self.timeA = timeToReach;

        """
        This means that this we were able to successfully signal.
        """
        #print("*****************Time Current&&&&&&&&&&&&&&: "+str(self.timeCurr));
        return True;




    def initState(self):
        """
        This initializes the state of the vertex based on
        indexBegin and indexEnd if it is a valid index
        """
        if self.containInputNodes():
            print(" Not a valid index for analysis");
            return False;

        """
        Find index of last activation
        """
        temp = self.findIndexLA(self.vIndex,self.indexBegin);
        if temp == -1:
            return False;
        self.indexLA = temp;
        self.timeLA = self.timeVec[self.indexLA];

        """
        Find index of next activation
        """
        temp = self.findIndexNA(self.vIndex,self.indexBegin);
        if temp == -1:
            return False;
        self.indexNA = temp;
        self.timeNA = self.timeVec[self.indexNA];
        """
        Initialize the current index
        """
        self.indexCurr = self.shiftLeft(self.vIndex, self.indexBegin);
        self.timeCurr = self.timeVec[self.indexCurr];

        """
        This vertex is currently active in the base case
        """
        if self.hNodeMot[self.vIndex][self.indexCurr] != 0 :
            self.isActive = True;
            self.prismLA = None;
            print("")
            print("Activated Vertex :"+str(self.vertexID));
            print("Current Time: "+str(self.timeCurr));
            sList = self.getSourceOfActivation(self.indexCurr);
            self.timeA = self.timeVec[self.indexCurr];
            self.sortListByTime(sList);
            self.initializeVCListActive(sList);
            return True;

        #Not currently active

        else:
            self.isActive = False;
            self.prismLA = None;
            self.timeCurr = self.timeVec[self.indexCurr];
            print("");
            print("Non-Active Vertex :"+str(self.vertexID));
            print("Current Time: "+str(self.timeCurr));
            print("Time of next activation: "+str(self.timeNA));
            sList = self.getSourceOfActivation(self.indexNA);
            self.printList(sList);
            self.sortListByTime(sList);
            self.initializeVCListNonActive(sList,self.timeCurr);
            return True;


#These are the helper methods:
    def updateVertex(self, timeCurr, vAindex):
        """
        Given that vA successfully signals this vertex,
        update the state.
        """
        print("Updating state of "+str(self.vertexID));
        timeToReach = timeCurr + self.TijMatrix[vAindex][self.vIndex];
        print("Current Threshold: "+str(self.cT));
        weightC = self.computeWeight(self.WijMatrix[vAindex][self.vIndex],timeToReach);
        wC = 1 -(weightC/self.cT);
        self.cT = self.cT - weightC;
        print("Threshold Afterwards: "+str(self.cT));
        elemToAppend = (vAindex+1, timeCurr, wC);
        self.vCList.append(elemToAppend);
        return

    def getSourceOfActivation(self, indexCurr):
        """
        This gives the list of nodes that activated this node
        and the times that it activated
        """
        listToReturn = []
        indexB = self.shiftLeft(self.vIndex,indexCurr);
        #print("Starting Elem is "+str(self.hNodeMot[self.vIndex][indexB]));
        vList = [];
        while(self.hNodeMot[self.vIndex][indexB]!= 0):
        #    print("Appending :"+str(self.hNodeMot[self.vIndex][indexB]));
            vList.append(self.hNodeMot[self.vIndex][indexB]);
            indexB = indexB +1;
        #print("=========");

        #Split into single versus duplicate activations
        listDuplicate = self.getDuplicates(vList);
        listSingle = self.getSingleton(vList);
        listSinglePair = self.getLASingletonList(listSingle,indexCurr);
        listDoublePair = self.getLADuplicateList(listDuplicate,vList,indexCurr);
        listToReturn = listSinglePair + listDoublePair;
        return listToReturn;

    def initializeVCListNonActive(self, list, timeCurr):
        """
        Given that it is not active currently and the current time
        this function initializes the VCList.
        Given, the next time of activation, it gets the time of those vertices
        that activated. If time is less than or equal to timeCurr, then
        append to the list.
        """
        initList = [];
        threshold = self.aN;
        self.cT = threshold;
        for i in range(len(list)):
            x = list[i];
            timeToReach = x[1] + self.TijMatrix[x[0]-1][self.vIndex];
            #Test for time condition
            if timeToReach <= timeCurr:
                weight = self.WijMatrix[x[0]-1][self.vIndex];
                weight = self.computeWeight(weight,timeToReach);
                wC = 1 - (weight/threshold);
                threshold = threshold - weight;
                print("Time signal arrive: "+str(timeToReach));
                print("Curr Time: "+str(timeCurr));
                elem = (x[0],x[1],wC);
                initList.append(elem);
        self.cT = threshold;
        self.vCList = initList;
        return;

    def initializeVCListActive(self, list):
        """
        This function initializes the VC list, given that it is
        currently active.
        """
        self.vCList.clear();
        threshold = self.aN;
        for x in range(len(list)):
            wTemp = self.WijMatrix[list[x][0]-1][self.vIndex];
            weight = self.computeWeight(wTemp,list[x][1]);
            #print("Weight:" +str(weight));
            wC = 1 - (weight/threshold);
            threshold = threshold - weight;
            elem =  (list[x][0], list[x][1], wC);
            self.vCList.append(elem);
        return;

    def findIndexLA(self,vIndex,indexCurr):
        """ Given, the vID index and the current index,
        this function finds the last index of activation
        """
        indexIter = self.shiftLeft(vIndex,indexCurr) - 1;
        indexBound = indexIter;
        iReturn = 0;
        #Iterates backwards to find the last activation
        for x in range(indexBound):
            if self.hNodeMot[vIndex][indexIter] != 0:
                iReturn = self.shiftLeft(vIndex,indexIter);
                #This checks if LA contains inputNodes
                if self.containINodesInterval(vIndex,iReturn,iReturn+self.aN):
                    print("Invalid LA")
                    return -1;
                else:
                    return iReturn;
            indexIter = indexIter - 1;

        print("Last Activation Index NA");
        return -1;

    def sortListByTime(self, list):
        """
        This function sorts the list based on the 2nd
        component of time
        """
        for x in range(len(list)):
            for y in range(x,len(list)):
                if list[x][1] > list[y][1]:
                    temp = list[x];
                    list[x] = list[y];
                    list[y] = temp;
        return;


    def getLASingletonList(self, listSingleton, indexCurr):
        """
        Given the list of singletons, this function returns
        the corresponding times that it was activated.
        """
        listToReturn = [];
        for x in range(len(listSingleton)):
            temp = self.findIndexLA(listSingleton[x]-1,indexCurr);
            if temp == -1:
                print("Error");
                return -1;
            time = self.timeVec[temp];
            elem = (listSingleton[x],time);
            listToReturn.append(elem);
        return listToReturn;

    def getLADuplicateList(self, listDuplicate, list,indexCurr):
        """
        This returns the ordered pair corresponding to duplicate list
        The ordered pair is the vertexID and the activation time
        """
        listToReturn = [];
        for i in range(len(listDuplicate)):
            elem = listDuplicate[i];
            num= self.getNumOfTimes(listDuplicate,elem);
            listElem = self.getElemMulTime(elem-1,num,indexCurr);
            if listElem == -1:
                print("Error");
                return -1;
            listToReturn = listToReturn + listElem;
        return listToReturn;


    def getElemMulTime(self,elemIndex, num, indexCurr):
        """
        Given the element, number of times that it occurs,
        and the current index, this function returns the ordered pair
        list with the vertexID and corresponding activation time.
        """
        listToReturn = [];
        indexIter = indexCurr;

        for i in range(num):
            tempI=self.findIndexLA(elemIndex,indexIter);
            if tempI == -1:
                print("Error");
                return -1;
            tTemp = self.timeVec[tempI];
            elem = (elemIndex +1, tTemp);
            listToReturn.append(elem);
            indexIter = tempI -1;

        return listToReturn;

    def getDuplicates(self, list):
        """
        This function gets the duplicate elements in the list
        """
        #Sort the list
        list.sort();
        listToReturn = [];
        elem = list[0];
        #Base case
        if len(list) == 1:
            return listToReturn;

        if list[0] == list[1]:
            listToReturn.append(elem);
        #Iterate through the list
        for x in range(len(list)-1):
            if list[x] == list[x+1] and list[x] != elem:
                listToReturn.append(list[x]);
                elem = list[x];

        return listToReturn;

    def getSingleton(self, list):
        """
        This function extracts the elements that don't repeat
        in the list.
        """
        list.sort();
        listToReturn = [];
        elemRepeat = None;
        #Base case
        if len(list) == 1:
            listToReturn.append(list[0]);
            return listToReturn;
        #Iterate through the loop
        for x in range(len(list)-1):
            if list[x] != list[x+1] and elemRepeat == None:
                listToReturn.append(list[x]);
            elif list[x] != list[x+1] and list[x]!= elemRepeat:
                listToReturn.append(list[x]);
            else:
                elemRepeat = list[x];
        #To account for the last element
        if list[len(list)-1] != list[len(list)-2]:
                listToReturn.append(list[len(list)-1]);
        return  listToReturn;

    def getNumOfTimes(self, list, elem):
        """
        This function get the number of times that the element
        occurs in the list.
        """
        count = 0;
        for x in range(len(list)):
            if list[x] == elem:
                count = count + 1;
        return count;

    def computeWeight(self, weight, time):
        """
        Given the weight and time, this function
        returns the adjusted weight.
        """
        return weight;

    def findIndexNA(self,vIndex,indexCurr):
        """
        Given the current index, this function finds
        the next index of activation.
        """
        indexIter = self.shiftRight(vIndex,indexCurr) + 1;
        for x in range(indexIter,self.indexEnd):
            if self.hNodeMot[vIndex][x] != 0:
                iReturn= x;
                if self.containINodesInterval(vIndex,iReturn, iReturn+self.aN):
                    print("Invalid NA");
                    return -1;
                else:
                    return iReturn;
        print("Next Activation Index NA");
        return -1;

    def containInputNodes(self):
        """
        This function checks if there are input nodes
        within the closed interval of indexBegin and indexEnd
        """
        #print("Here");
        for i in range(self.numOfVertices):
            for j in range(self.indexBegin, self.indexEnd):
                if self.hNodeMot[i][j] == -1:
                    #print("["+str((i))+","+str(j)+"]");
                    #print("Time :" +str(self.timeVec[j]));
                    return True;
        return False;

    def containINodesInterval(self, vIndex, indexBegin, indexEnd):
        """
        Given the vID index, index begin, and index end, this
        function returns true if there are input nodes in the interval.
        Otherwise, return false
        """
        for i in range(indexBegin,indexEnd):
            if self.hNodeMot[vIndex][indexBegin+i] == -1:
                return True;
        return False;

    def shiftLeft(self, vIndex, currIndex):
        """
        This function returns the currIndex
        shifted to the left
        """
        indexToReturn = currIndex;
        for x in range(self.aN+1):
                #print(str(x)+"--"+str(self.hNodeMot[vIndex][indexToReturn]));
                if self.hNodeMot[vIndex][indexToReturn] == 0:
                #    print("---------");
                    return indexToReturn + 1;
                indexToReturn = indexToReturn-1;
        print("Should not execute here. Shift Left")
        return indexToReturn;

    def shiftRight(self, vIndex, currIndex):
        """
        This function returns the currIndex
        shifted to the right
        """
        indexToReturn = currIndex;
        for x in range(self.aN+1):
                #print(str(x)+"--"+str(self.hNodeMot[vIndex][indexToReturn]));
                if self.hNodeMot[vIndex][indexToReturn] == 0:
                    return indexToReturn - 1;
                indexToReturn = indexToReturn+1;
        print("Should not execute here.  Shift right");
        return indexToReturn;

    def checkIfNextTime(self, timeToCheck):
        """
        This function checks if the time is right next
        to the current time
        """
        index = 0;
        elem = self.timeVec[self.indexCurr];
        print("Current Time :" + str(elem));
        print("Time to check:" + str(timeToCheck));
        while(self.timeVec[self.indexCurr+index]== elem):
            index = index + 1;
        #End of the loop
        if self.timeVec[self.indexCurr+index] == timeToCheck:
            return True;
        else:
            return False;

    def printState(self):
        """
        This function prints the state of vertex
        """
        print("************************");
        print(" Vertex: " + str(self.vertexID));
        print(" Is Active: " + str(self.isActive));
        if self.isActive:
            print(" Time Activate: " + str(self.timeA));
        print(" # of elem in vCList: " + str(len(self.vCList)));
        for x in range(len(self.vCList)):
            print(str(self.vCList[x]));
        return;

    def printList(self,list):
        """
        This helper function prints the element in the lsit
        """
        for x in range(len(list)):
            print(str(list[x]));
