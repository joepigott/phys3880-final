import sys
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams.update({"font.size": 12})

data = pd.read_csv(sys.argv[1])

print("Number of data points: ", len(data))

# determine which title to use based on metadata

if "start" in data.columns:
    start = data["start"].values[0]
    end = data["end"].values[0]
    if "hour" in data.columns and not np.isnan(data["hour"].values[0]):
        hour = 2 * int(data["hour"].values[0])
        title = f"Pressure Spectrum Magnitude from {start} to {end}, hours {hour} - {hour + 2}"
    else:
        title = f"Pressure Spectrum Magnitude from {start} to {end}"
else:
    title = "Pressure Spectrum Magnitude"

magnitude = data["magnitude"].values
frequencies = data["freq"].values

plt.plot(frequencies[:100], magnitude[:100])
plt.title(title)
plt.xlabel("Frequency (cycles/minute)")
plt.ylabel("Magnitude")
plt.ylim(-1, 1) # for plotting level 4 data
plt.show()
