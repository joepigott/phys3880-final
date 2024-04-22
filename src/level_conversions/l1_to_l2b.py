# convert level 1 (relative) data to level 2b (padded fft) data

import argparse
import pandas as pd
import scipy
import numpy as np

SAMPLE_RATE = 1 # 1 per minute before 2024-04-11
# SAMPLE_RATE = 2 # 2 per minute past 2024-04-11

# the number of times the data will be padded
PADDING_FACTOR = 5

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, required=True)
parser.add_argument("files", nargs=argparse.REMAINDER)
args = parser.parse_args()

if args.output[-1] != "/":
    args.output += "/"

first = True
for file in args.files:
    raw = pd.read_csv(file)

    values = raw["value"].values
    values = np.pad(values, (0, len(values) * PADDING_FACTOR - len(values)), "constant")

    # perform fft
    fft = scipy.fft.rfft(values)
    magnitude = np.abs(fft)
    fft_freq = scipy.fft.rfftfreq(len(values), d=1./SAMPLE_RATE)

    # save data
    data = pd.DataFrame({
        "magnitude": magnitude,
        "freq": fft_freq,
    })
    
    # resize start, end, and hour columns to fit new dataframe
    start = [raw["start"].values[0]]
    end = [raw["end"].values[0]]
    hour = [raw["hour"].values[0]]

    for _ in range(len(data) - 1):
        start.append("")
        end.append("")
        hour.append("")

    data["start"] = start
    data["end"] = end
    data["hour"] = hour

    filename = file.split("/")[-1].replace("l1", "l2b")
    data.to_csv(args.output + filename, index=False)
