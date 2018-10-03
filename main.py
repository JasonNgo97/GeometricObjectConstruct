import numpy as np
import csv
from GeoConstruct import *

print("Hello");
#x = GeoConstruct(10,20);
numVertices = 5;
height = 10;
radius = 6;
angle = 70;
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
# W e initialize the matrices using this
geoTempGraph.initializeMatrices(motFinal,tstFinal,wgtFinal);
