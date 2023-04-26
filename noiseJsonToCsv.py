import sys
import json

jsonFile = sys.argv[1]
dataset = jsonFile.split(".")[0]

file = open(jsonFile, "r")
jsonData = json.loads(file.read())
file.close()

distances = []

experimentIndex = 0

for originalObject in jsonData.keys():
    if(not ".obj" in originalObject): continue
    for comparisonObject in jsonData[originalObject].keys():
        for distance in jsonData[originalObject][comparisonObject]["noiseFloors"]:
            distances.append({
                "originalObject": originalObject, 
                "comparisonObject": comparisonObject, 
                "distance": distance, 
                "experimentIndex": experimentIndex, 
                "vertexCount": len(jsonData[originalObject][comparisonObject]["noiseFloors"])})
        
        experimentIndex += 1

distancesCSV = open("3DSC" + "_vertex_distances.csv", "w")
distancesCSV.write("originalObject,comparisonObject,distance,experimentIndex,vertexCount\n")
for row in distances:
    distancesCSV.write(row["originalObject"] + "," + row["comparisonObject"] + "," + str(row["distance"]) + "," + str(row["experimentIndex"]) + "," + str(row["vertexCount"]) + "\n")
distancesCSV.close()
