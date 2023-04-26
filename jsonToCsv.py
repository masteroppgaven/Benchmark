import sys
import json

jsonFile = sys.argv[1]
dataset = jsonFile.split(".")[0]

file = open(jsonFile, "r")
jsonData = json.loads(file.read())
file.close()

generationTimes = []
vertexCounts = []
similarities = []

for object in jsonData["results"].keys():
    for dataset in jsonData["results"][object].keys():
      for descriptor in jsonData["results"][object][dataset].keys():
            if(descriptor == "vertexCounts"): continue
            for category in jsonData["results"][object][dataset][descriptor].keys():
                # generationTime burde egentlig være inne under category, fiks når det dataen er sånn
                generationTimes.append({"dataset": dataset, "object": object, "descriptor": descriptor, "category": category ,"time": jsonData["results"][object][dataset][descriptor][category]["generationTime"]})

for object in jsonData["results"].keys():
    for dataset in jsonData["results"][object].keys():
        for category in jsonData["results"][object][dataset]["vertexCounts"].keys():
            # generationTime burde egentlig være inne under category, fiks når det dataen er sånn
            vertexCounts.append({"dataset": dataset, "object": object, "category": category, "vertexCount": jsonData["results"][object][dataset]["vertexCounts"][category]["vertexCount"]})

for object in jsonData["results"].keys():
    for dataset in jsonData["results"][object].keys():
      for descriptor in jsonData["results"][object][dataset].keys():
            if(descriptor == "vertexCounts"): continue
            for category in jsonData["results"][object][dataset][descriptor].keys():
                for distanceFunction in jsonData["results"][object][dataset][descriptor][category].keys():
                    if(distanceFunction == "generationTime"): continue
                    similarities.append({"dataset": dataset, "object": object, "descriptor": descriptor, "category": category, "distanceFunction": distanceFunction, "time": jsonData["results"][object][dataset][descriptor][category][distanceFunction]["time"], "similarity": jsonData["results"][object][dataset][descriptor][category][distanceFunction]["similarity"]})

generationTimes = sorted(generationTimes, key=lambda k: (k['category'], k['object']))
vertexCounts = sorted(vertexCounts, key=lambda k: (k['category'], k['object']))
similarities = sorted(similarities, key=lambda k: (k['category'], k['object']))
similarities = sorted(similarities, key=lambda k: (k['distanceFunction']))

generationTimesCSV = open(dataset + "_generationTimes.csv", "w")
generationTimesCSV.write("dataset,object,descriptor,category,time\n")
for row in generationTimes:
    generationTimesCSV.write(row["dataset"] + "," + row["object"] + "," + row["descriptor"] + "," + row["category"] + "," + str(row["time"]) + "\n")

generationTimesCSV.close()

vertexCountsCSV = open(dataset + "_vertexCounts.csv", "w")
vertexCountsCSV.write("dataset,object,category,vertexCount\n")
for row in vertexCounts:
    vertexCountsCSV.write(row["dataset"] + "," + row["object"] + "," + row["category"] + ","+ str(row["vertexCount"]) + "\n")

vertexCountsCSV.close()

similarityCSV = open(dataset + "_similarity.csv", "w")
similarityCSV.write("dataset,object,descriptor,category,distanceFunction,time,similarity\n")
for row in similarities:
    similarityCSV.write(row["dataset"] + "," + row["object"] + "," + row["descriptor"] + "," + row["category"] + "," + row["distanceFunction"] + "," + str(row["time"]) + "," + str(row["similarity"]) + "\n")

similarityCSV.close()
