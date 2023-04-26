import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = []

file = open("noisefloor/QUICCI_vertex_distances.csv", "r")
reader = csv.reader(file, delimiter=",")
next(reader, None)
for line in reader:
    # None of the distance functions can get anything lower than -1, but use -2 to compensate for inaccuracies with float values:)
    if not line[2] == "None" and float(line[2]) >= -2:
        data.append([line[0], line[1], float(line[2]), int(line[3]), int(line[4])])
file.close()
data.pop(0)

standardDeviations = {}
for line in data:
    standardDeviations.setdefault(line[3], []).append(line[2])
for key in standardDeviations.keys():
    standardDeviations[key] = np.std(standardDeviations[key])

totalStdDev = 0
for key in standardDeviations.keys():
    totalStdDev += standardDeviations[key]

averageStdDev = totalStdDev / len(standardDeviations.keys())

print("Average Standard Deviation: " + str(averageStdDev))

# df = pd.DataFrame({"experimentID": standardDeviations.keys(), "standardDeviation": [standardDeviations[key] for key in standardDeviations.keys()]})

plt.figure().set_figwidth(10)  
plt.axhline(y=averageStdDev, color='r', linestyle='-', label='Average Standard Deviation')
# plt.plot('experimentID', 'standardDeviation', data=df, linestyle='none', marker='o', markersize=1.2)

plt.legend()

plt.bar(standardDeviations.keys(), [standardDeviations[key] for key in standardDeviations.keys()])

plt.xlabel("Experiment ID")
plt.ylabel("Standard Deviation")

# plt.axis([0, max(df['experimentID']), -2, 2])

plt.show()