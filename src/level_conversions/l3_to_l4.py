# given a list of spectra, find the spectral peak between the relevant
# frequencies and compile them into a distribution

import argparse
import pandas as pd

# range of frequencies (cycles/min) to consider
RANGE_START = 0.033 # period of 30 minutes
RANGE_END = 0.1 # period of 10 minutes

argparser = argparse.ArgumentParser()
argparser.add_argument("--output", type=str, required=True)
argparser.add_argument("files", nargs=argparse.REMAINDER)
args = argparser.parse_args()

if args.output[-1] != "/":
    args.output += "/"

peaks = []
freqs = []
starts = []
ends = []
hours = []

# first file is named `l3a_pressure_2024-03-25_2024-04-09_0.csv`. output name
# should remove the last integer and replace `l3` with `l4`
filename = args.files[0].split("/")[-1].split(".")[0].replace("l3", "l4")[0:-2] + ".csv"

for file in args.files:
    data = pd.read_csv(file)

    starts.append(data["start"].values[0])
    ends.append(data["end"].values[0])
    hours.append(data["hour"].values[0])

    # find the peak between the relevant frequencies
    data = data[(data["freq"] >= RANGE_START) & (data["freq"] <= RANGE_END)]
    peak = data.loc[data["magnitude"].idxmax()]

    freqs.append(peak["freq"])
    peaks.append(peak["magnitude"])

result = pd.DataFrame({
    "freq": freqs,
    "magnitude": peaks,
    "start": starts,
    "end": ends,
    "hour": hours
})

result.to_csv(args.output + filename, index=False)
