import os
import sys
import json
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
                        "stdDev": jsonData["results"][originalObject][dataset][shapeDescriptor][category][distanceFunction]["stdDeviation"],
                        "vertexCount": jsonData["results"][originalObject][dataset][shapeDescriptor][category][distanceFunction]["objectData"]["comparisonVertexCount"]}
                    )

for chosenShapeDescriptor in shapeDescriptors.keys():
    categories = pd.DataFrame({"category": [test["category"] for test in shapeDescriptors.get("RICI")]})
    categories = categories.drop_duplicates()
    categories = categories.reset_index(drop=True)
    categories = categories["category"].tolist()

    for category in categories:
        df = pd.DataFrame({"averageDistance": [test["avgDis"] for test in shapeDescriptors.get(chosenShapeDescriptor)],
                               "vertexCount": [test["vertexCount"] for test in shapeDescriptors.get(chosenShapeDescriptor)],
                               "category": [test["category"] for test in shapeDescriptors.get(chosenShapeDescriptor)],
                               "stdDeviation": [test["stdDev"] for test in shapeDescriptors.get(chosenShapeDescriptor)]})
        df.sort_values(by=["averageDistance"], inplace=True)
        df = df.reset_index(drop=True)

        dfStdDev = pd.DataFrame({"stdDeviation":  [test["stdDev"] for test in shapeDescriptors.get(chosenShapeDescriptor)],
                               "vertexCount": [test["vertexCount"] for test in shapeDescriptors.get(chosenShapeDescriptor)],
                               "category": [test["category"] for test in shapeDescriptors.get(chosenShapeDescriptor)]})
        dfStdDev.sort_values(by=["stdDeviation"], inplace=True)
        dfStdDev = dfStdDev.reset_index(drop=True)

        df.drop(df[df.category != category].index, inplace=True)
        dfStdDev.drop(dfStdDev[dfStdDev.category != category].index, inplace=True)

        plt.figure().set_figwidth(10)
        plt.rcParams['font.size'] = 14
        plt.title(chosenShapeDescriptor +' - ' + datasetName + ' - ' + category, fontstyle='italic')

        print("Category: " + category + ", " + "Shape Descriptor: " + chosenShapeDescriptor + ", " + "Mean distance: " + str(df["averageDistance"].mean()))

        plt.plot('averageDistance', data=df, linestyle="none", marker='o', markersize=2, color=colours[chosenShapeDescriptor], label="Average Distance")
        plt.plot('stdDeviation', data=df, linestyle="none", marker='o', markersize=2, color="tab:green", label="Average Standard Deviation")
        plt.axhline(y=stdDev[chosenShapeDescriptor], color="tab:red", linewidth=3, linestyle="dotted", label="Standard Deviation Boundary")
        plt.axhline(y=noise[chosenShapeDescriptor], color="tab:cyan", linewidth=3, linestyle="dotted", label="Poor Performance Matching Boundary")
        
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
              fancybox=True, shadow=True, ncol=2)
    
        # plt.yscale('log')

        plt.margins(0)
        plt.tight_layout()

        plt.xlabel("Object Index")
        plt.ylabel("Distance")

        folderPath = "imagesVertex/" + datasetName + "/"

        if not os.path.exists(folderPath):
            os.makedirs(folderPath)

        plt.savefig(folderPath + chosenShapeDescriptor + "_"  + category + "_" + datasetName + "_comparisonVertexGraph.png", bbox_inches='tight')
        plt.close()
