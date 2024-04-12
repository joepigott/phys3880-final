import argparse
import pandas as pd
import scipy
import numpy as np

# l1 data is relative pressure. l2a data will be the fft of the raw l1 data.

# SAMPLE_RATE = 1 # 1 per minute before 2024-04-11
SAMPLE_RATE = 2 # 2 per minute past 2024-04-11

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, required=True)
parser.add_argument("files", nargs=argparse.REMAINDER)
args = parser.parse_args()

if args.output[-1] != "/":
    args.output += "/"

first = True
for file in args.files:
    raw = pd.read_csv(file)

    values = raw["rel_pressure"].values

    # perform fft
    fft = scipy.fft.rfft(values)
    magnitude = np.abs(fft)

    # returns frequencies as cycles per unit of sample rate (minute)
    fft_freq = scipy.fft.rfftfreq(len(values), d=1./SAMPLE_RATE)

    # save data
    data = pd.DataFrame({
        "magnitude": magnitude,
        "freq": fft_freq,
    })

    if "start" in raw.columns:
        start = [raw["start"].values[0]]
        end = [raw["end"].values[0]]

        for _ in range(len(data) - 1):
            start.append("")
            end.append("")

        data["start"] = start
        data["end"] = end

    if "hour" in raw.columns:
        hour = [raw["hour"].values[0]]

        for _ in range(len(data) - 1):
            hour.append("")

        data["hour"] = hour

    filename = file.split("/")[-1].replace("l1", "l2a")
    data.to_csv(args.output + filename, index=False)
