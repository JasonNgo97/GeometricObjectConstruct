import numpy as np
import csv
from GeoConstruct import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.lines as mlines


print("Hello");
#x = GeoConstruct(10,20);
numVertices = 12;
height = 20;
radius = 6;
angle = 70;
s_ij = 0.1
beginHIndex = 784;
endHIndex = 789
geoTempGraph = GeoConstruct(numVertices, height, radius, angle);
print ("Num of Vertices"+ str(geoTempGraph.NumberOfVertices));
rowCount = 0;

#Here we parse the files and load the matrices
with open('Mot.csv') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',');
    mot = list(csvReader);
    motFinal = np.array(mot).astype("float");
    print(" First row of Mot ");
    print(motFinal[0,:]);

with open('Tst.csv') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',');
    tst = list(csvReader);
    tstFinal = np.array(tst).astype("float");
    print(" First row of Tst");
    print(tstFinal[0,:]);

with open('Wgt.csv') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',');
    wgt = list(csvReader);
    wgtFinal = np.array(wgt).astype("float");
    print(" First row of Wgt");
    print(wgtFinal[0,:]);

with open('Dij.csv') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',');
    dij = list(csvReader);
    dijFinal = np.array(dij).astype("float");
    print(" First row of dij");
    print(dijFinal[784:]);
# We initialize the matrices using this
geoTempGraph.initializeMatrices(motFinal,tstFinal,wgtFinal);

#Here I'm truncating the matrix to only analyze the hidden nodes
tempMat=np.array(motFinal);

#This initializes the Mot File for hidden Nodes
hiddenNodeMot=tempMat[beginHIndex:endHIndex,:];
print(hiddenNodeMot[1,1000:2000]);
print("Dimension Length" + str(hiddenNodeMot.shape[0]));

for i in range(0,hiddenNodeMot.shape[0]):
    for j in range(0,hiddenNodeMot.shape[1]):
        if hiddenNodeMot[i][j] >= 785 and hiddenNodeMot[i][j]<=789:
            hiddenNodeMot[i][j] = hiddenNodeMot[i][j] - 784;
        else:
            hiddenNodeMot[i][j] = 0;

#print("The first row of converted matrix")
hiddenNodeMotFinal=np.array(hiddenNodeMot).astype("int");
#print("The first row of converted matrix")
#print(hiddenNodeMotFinal[0,1000:2000]);


#This initializes the tst Fie for hidden Nodes
tempMat = np.array(tstFinal);
hiddenNodeTstFinal = tempMat[beginHIndex:endHIndex,:];
tempMat = np.array(dijFinal);
dijHNode= tempMat[beginHIndex:endHIndex,beginHIndex:endHIndex];

print(" Dij of Hidden Nodes");
for i in range(0,dijHNode.shape[0]):
    print(dijHNode[i,0:dijHNode.shape[1]]);
#Now, we need to initialize the Tij matrix


TijHNode=dijHNode;
for i in range(0, TijHNode.shape[0]):
    for j in range(0, TijHNode.shape[1]):
        TijHNode[i][j]=TijHNode[i][j]/s_ij;

print(" Time delay of Hidden Nodes");

for i in range(0, TijHNode.shape[0]):
    print(TijHNode[i,0:TijHNode.shape[1]]);


geoTempGraph.initializeHNodeMatrix(hiddenNodeMotFinal,hiddenNodeTstFinal,TijHNode);

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#geoTempGraph.initializeFirstBn(ax);

geoTempGraph.initializePrism(ax,(0,0,1));
plt.show();
