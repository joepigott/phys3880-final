import sys
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

matplotlib.rcParams.update({'font.size': 12})

# load the data
data = pd.read_csv(sys.argv[1])

pressure = data["value"]
dates = data["created_at"]

# convert from strings to dates
dates = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S %Z") for d in dates]

# plot data
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
plt.title("Barometric Pressure (hPa)")
plt.xlabel("Time")
plt.ylabel("Pressure (hPa)")
plt.grid()
plt.plot(dates, pressure)
plt.show()
