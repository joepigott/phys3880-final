import argparse
import pandas as pd
import scipy
import numpy as np

# l1 data is relative pressure. l2b data will be the fft of the padded l1 data.

# sample rate is 1 per minute. this may change
SAMPLE_RATE = 2

# the number of times the data will be padded
PADDING_FACTOR = 10

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
