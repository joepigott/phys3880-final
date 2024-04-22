# this program performs the actual analysis of the transformed data. input
# should be a level 4 file, which contains a distribution of spectral peaks
# within the range of 0.033 to 0.1 cycles/min, relative to the average 
# spectrum.
#
# the program will check for values that are more than 3 standard deviations
# away from the mean in the positive direction, which are significant peaks
# signifying possible detection of an atmospheric gravity wave. the value,
# frequency, and time of these peaks will be printed to the console.

import sys
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import datetime

file = sys.argv[1]
data = pd.read_csv(file)

print(f"Analyzing {file}...")

print(f"File ranges from {data['start'][0]} to {data['end'][0]}")

# determine the standard deviation and check for values that are more than 3
# standard deviations away
stdev = data["magnitude"].std()
mean = data["magnitude"].mean()
threshold = mean + 3 * stdev
print(f"Mean: {mean:.3f} hPa, Standard Deviation: {stdev:.3f} hPa, Threshold: {threshold:.3f} hPa")

print("\nPossible wave detections:")
for index, row in data.iterrows():
    if row["magnitude"] > threshold:
        print(f"\tPossible wave detected at hour index {row['hour']}")

        date = datetime.datetime.strptime(row["start"], "%Y-%m-%d")
        start = date + datetime.timedelta(hours = (2 * row['hour']))
        end = start + datetime.timedelta(hours = 2)

        start = start.strftime('%Y-%m-%d %H:%M')
        end = end.strftime('%Y-%m-%d %H:%M')
        print(f"\t\tMagnitude: {row['magnitude']:.3f} hPa")
        print(f"\t\tFrequency: {row['freq']:.3f} cycles/min")
        print(f"\t\tTime: between {start} and {end}\n")

matplotlib.rcParams.update({"font.size": 14})

_, bins, _ = plt.hist(data["magnitude"])
plt.title(f"Spectral peaks relative to the average, from 0.033 to 0.1 cycles/min, \n from {data['start'][0]} to {data['end'][0]}")
plt.xlabel("Magnitude (hPa)")
plt.ylabel("Count")

# each bin should be labeled
plt.xticks(bins)

plt.grid()
plt.show()
