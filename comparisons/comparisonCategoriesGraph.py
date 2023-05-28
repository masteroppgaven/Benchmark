import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

jsonFile = sys.argv[1]
datasetName = jsonFile.split(".")[0]
datasetName = datasetName.split("/").pop()

file = open(jsonFile, "r")
jsonData = json.loads(file.read())
file.close()

noiseRICI = 52 #148
noiseQUICCI = 513 #1027
noiseSI = 0.49 #0.19
noise3DSC = 3.58 #8
noiseFPFH = 342.4 #982

stdDevRICI = 70
stdDevQUICCI = 278
stdDevSI = 0.2
stdDev3DSC = 1.9
stdDevFPFH = 151

noise = {"RICI": noiseRICI, "QUICCI": noiseQUICCI, "SI": noiseSI, "3DSC": noise3DSC, "FPFH": noiseFPFH}
stdDev = {"RICI": stdDevRICI, "QUICCI": stdDevQUICCI, "SI": stdDevSI, "3DSC": stdDev3DSC, "FPFH": stdDevFPFH}
shapeDescriptors = {"RICI": [], "QUICCI": [], "SI": [], "3DSC": [], "FPFH": []}

colours = ["tab:blue", "tab:orange", "tab:gray", "tab:pink", "tab:purple"]
colours = {"RICI": colours[0], "QUICCI": colours[1], "SI": colours[2], "3DSC": colours[3], "FPFH": colours[4]}

# [Object Number, Category, Average Distance, Standard Deviation]
for originalObject in jsonData["results"].keys():
    for dataset in jsonData["results"][originalObject].keys():
        for shapeDescriptor in jsonData["results"][originalObject][dataset].keys():
            if shapeDescriptor ==  "vertexCounts": continue
            for category in jsonData["results"][originalObject][dataset][shapeDescriptor].keys():
                for distanceFunction in jsonData["results"][originalObject][dataset][shapeDescriptor][category].keys():
                    if distanceFunction == "generationTime": continue
                    shapeDescriptors.get(shapeDescriptor).append({
                        "object": int(originalObject),
                        "category": category,
                        "avgDis": jsonData["results"][originalObject][dataset][shapeDescriptor][category][distanceFunction]["averageDistance"],
                        "stdDev": jsonData["results"][originalObject][dataset][shapeDescriptor][category][distanceFunction]["stdDeviation"]}
                    )

for chosenShapeDescriptor in shapeDescriptors.keys():
    df = pd.DataFrame({"category":[int(test["category"]) if test["category"].isdigit() else test["category"] for test in shapeDescriptors.get(chosenShapeDescriptor)], 
                        "averageDistance":  [test["avgDis"] for test in shapeDescriptors.get(chosenShapeDescriptor)]})
    dfMean = df.groupby('category')['averageDistance'].mean()
    dfMean = dfMean.to_frame().reset_index()

    dfStdDev = pd.DataFrame({"category": [int(test["category"]) if test["category"].isdigit() else test["category"] for test in shapeDescriptors.get(chosenShapeDescriptor)], 
                           "stdDeviation":  [test["stdDev"] for test in shapeDescriptors.get(chosenShapeDescriptor)]})
    dfStdDevMean = dfStdDev.groupby('category')['stdDeviation'].mean()
    dfStdDevMean = dfStdDevMean.to_frame().reset_index()
    
    # Need this as the 5.1-15.0 category is sorted in the wrong order
    if datasetName == "OverlappingObjects":
        overlappingCategories = pd.CategoricalDtype(['0', '5.1-15.0', '15.1-25.0', '25.1-35.0', '35.1-45.0', '45.1-55.0', '55.1-65.0', '65.1-75.0', '75.1-85.0', '85.1-95.1'], ordered=True)
        dfMean['category'] = dfMean['category'].astype(overlappingCategories)
        dfStdDevMean['category'] = dfMean['category'].astype(overlappingCategories)

    if datasetName == "RotatedObjectsDatset":
        rotatedCategories = pd.CategoricalDtype(['0', 'X', 'Y', 'Z', 'XYZ'], ordered=True)
        dfMean['category'] = dfMean['category'].astype(rotatedCategories)
        dfStdDevMean['category'] = dfMean['category'].astype(rotatedCategories)

    if datasetName == "MovedObjectsDataset":
        rotatedCategories = pd.CategoricalDtype(['0', 'SmallMove-0.2f', 'BigMove-10.0f'], ordered=True)
        dfMean['category'] = dfMean['category'].astype(rotatedCategories)
        dfStdDevMean['category'] = dfMean['category'].astype(rotatedCategories)


    startDistance = 0
    if chosenShapeDescriptor == "SI":
        startDistance = 1

    dfMean.sort_values(by=["category"], inplace=True)
    dfStdDevMean.sort_values(by=["category"], inplace=True)

    # We have already done the noiseroof tests, and found out that the shape descriptors
    # are capable of getting a perfect score when two equal objects are compared.
    newMeanRow = {"category": 0, "averageDistance": startDistance}
    dfMean = pd.concat([pd.DataFrame(newMeanRow, index=[0]), dfMean], ignore_index=True).reset_index(drop=True)

    newStdRow = {"category": 0, "stdDeviation": 0}
    dfStdDevMean = pd.concat([pd.DataFrame(newStdRow, index=[0]), dfStdDevMean], ignore_index=True).reset_index(drop=True)

    dfMean["category"] = dfMean["category"].astype(str)
    dfStdDevMean["category"] = dfStdDevMean["category"].astype(str)

    plt.figure().set_figwidth(10)
    plt.rcParams['font.size'] = 14
    plt.xticks(fontsize=12)
    plt.title(chosenShapeDescriptor +' - ' + datasetName, fontstyle='italic')

    plt.plot('category', 'averageDistance', data=dfMean, marker='o', markersize=2, linewidth=2, color=colours[chosenShapeDescriptor], label="Average Distance")
    plt.plot('category', 'stdDeviation', data=dfStdDevMean, marker='o', markersize=2, linewidth=2, color="tab:green", linestyle="dashed", label="Average Standard Deviation")

    plt.axhline(y=stdDev[chosenShapeDescriptor], color="tab:red", linestyle="dotted", linewidth=3, markersize=8, label="Standard Deviation Boundary")
    plt.axhline(y=noise[chosenShapeDescriptor], color="tab:cyan", linestyle="dotted", linewidth=3, markersize=8, label="Poor Performance Matching Boundary")

    plt.xticks(dfMean['category'])

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
              fancybox=True, shadow=True, ncol=2)
    
    plt.ylim(bottom=0)

    plt.margins(0)
    plt.tight_layout()
    plt.grid()

    plt.xlabel("Degree of Holes")
    plt.ylabel("Distance")

    folderPath = "imagesCategories/" + datasetName + "/"

    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    plt.savefig(folderPath + chosenShapeDescriptor + "_" + datasetName + "_comparisonCategoriesGraph.png", bbox_inches='tight')
    plt.close()
