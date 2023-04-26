import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

data = []

file = open("noisefloor/SI_vertex_distances.csv", "r")
reader = csv.reader(file, delimiter=",")
next(reader, None)
for line in reader:
    # None of the distance functions can get anything lower than -1, but use -2 to compensate for inaccuracies with float values:)
    if not line[2] == "None" and float(line[2]) >= -2:
        data.append([line[0], line[1], float(line[2]), int(line[3]), int(line[4])])
file.close()
data.pop(0)

# data = sorted(data, key=lambda x: x[4], reverse=False)

# currentIndex = 0
# previousIndex = -1
# for line in data:
#    if line[3] != previousIndex:
#        currentIndex += 1
#        previousIndex = line[3]
    
#    line[3] = currentIndex

# data = np.array(data, dtype="O")

averageDistance = 0
for distance in data:
    averageDistance += distance[2]
averageDistance /= len(data)

ninetythPercentile = np.percentile([distance[2] for distance in data], 10)
# ninetythPercentile = np.percentile([distance[2] for distance in data], 90)

print("Total Average: " + str(averageDistance) + " (Red)")
print("10th Percentile: " + str(ninetythPercentile) + " (Pink)")
# print("90th Percentile: " + str(ninetythPercentile) + " (Green)")

df = pd.DataFrame({"experimentID": [distance[3] for distance in data], "distance": [distance[2] for distance in data]})

plt.figure().set_figwidth(10)  
plt.axhline(y=averageDistance, color='r', linestyle='-')
plt.axhline(y=ninetythPercentile, color='green', linestyle='--')
plt.plot('experimentID', 'distance', data=df, linestyle='none', marker='o', markersize=1.2)

plt.xlabel("Experiment ID")
plt.ylabel("Distance")

plt.show()