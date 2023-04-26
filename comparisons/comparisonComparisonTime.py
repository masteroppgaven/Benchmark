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
                        "comparisonTime": jsonData["results"][originalObject][dataset][shapeDescriptor][category][distanceFunction]["time"],
                        "vertexCount": jsonData["results"][originalObject][dataset][shapeDescriptor][category][distanceFunction]["objectData"]["originalFaceCount"]}
                    )

dfRICI = pd.DataFrame({"comparisonTime": [test["comparisonTime"] for test in shapeDescriptors.get("RICI")],
                        "vertexCount": [test["vertexCount"] for test in shapeDescriptors.get("RICI")]})
dfRICI.sort_values(by=["comparisonTime"], inplace=True)
dfRICI = dfRICI.reset_index(drop=True)

print("RICI Mean: " + str(dfRICI["comparisonTime"].mean()))

dfQUICCI = pd.DataFrame({"comparisonTime": [test["comparisonTime"] for test in shapeDescriptors.get("QUICCI")],
                        "vertexCount": [test["vertexCount"] for test in shapeDescriptors.get("QUICCI")]})
dfQUICCI.sort_values(by=["comparisonTime"], inplace=True)
dfQUICCI = dfQUICCI.reset_index(drop=True)

print("QUICCI Mean: " + str(dfQUICCI["comparisonTime"].mean()))

dfSI = pd.DataFrame({"comparisonTime": [test["comparisonTime"] for test in shapeDescriptors.get("SI")],
                    "vertexCount": [test["vertexCount"] for test in shapeDescriptors.get("SI")]})
dfSI.sort_values(by=["comparisonTime"], inplace=True)
dfSI = dfSI.reset_index(drop=True)

print("SI Mean: " + str(dfSI["comparisonTime"].mean()))

df3DSC = pd.DataFrame({"comparisonTime": [test["comparisonTime"] for test in shapeDescriptors.get("3DSC")],    
                        "vertexCount": [test["vertexCount"] for test in shapeDescriptors.get("3DSC")]})
df3DSC.sort_values(by=["comparisonTime"], inplace=True)
df3DSC = df3DSC.reset_index(drop=True)

print("3DSC Mean: " + str(df3DSC["comparisonTime"].mean()))

dfFPFH = pd.DataFrame({"comparisonTime": [test["comparisonTime"] for test in shapeDescriptors.get("FPFH")],
                        "vertexCount": [test["vertexCount"] for test in shapeDescriptors.get("FPFH")]})
dfFPFH.sort_values(by=["comparisonTime"], inplace=True)
dfFPFH = dfFPFH.reset_index(drop=True)

print("FPFH Mean: " + str(dfFPFH["comparisonTime"].mean()))

plt.figure().set_figwidth(10)
plt.title("Comparison Time", fontstyle='italic')
plt.xlabel("Object #")
plt.ylabel("Comparsion Time (s)")

plt.plot(dfRICI["comparisonTime"], color=colours.get("RICI"), label="RICI", linestyle="none", marker="o", markersize=2)
plt.plot(dfQUICCI["comparisonTime"], color=colours.get("QUICCI"), label="QUICCI", linestyle="none", marker="o", markersize=2)
plt.plot(dfSI["comparisonTime"], color=colours.get("SI"), label="SI", linestyle="none", marker="o", markersize=2)
plt.plot(df3DSC["comparisonTime"], color=colours.get("3DSC"), label="3DSC", linestyle="none", marker="o", markersize=2)
plt.plot(dfFPFH["comparisonTime"], color=colours.get("FPFH"), label="FPFH", linestyle="none", marker="o", markersize=2)

plt.margins(0)
plt.tight_layout()
plt.grid()

plt.legend()
plt.savefig("comparisonTime/" + "ComparisonTime.png")