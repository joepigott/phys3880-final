# given a list of files with normalized hourly spectra, compute the average
# spectrum

import argparse
import pandas as pd
import numpy as np

argparser = argparse.ArgumentParser()
argparser.add_argument("--output", type=str, required=True)
argparser.add_argument("files", type=str, nargs=argparse.REMAINDER)
args = argparser.parse_args()

if args.output[-1] != "/":
    args.output += "/"

# determine the file name
filename = args.files[0].split("/")[-1].split(".")[0]
filename = "_".join(filename.split("_")[:-1]) + "_average.csv"

values = []
frequency = []
for file in args.files:
    data = pd.read_csv(args.files[0])

    if len(values) == 0:
        values = np.zeros(len(data["magnitude"]))

    for i, value in enumerate(data["magnitude"]):
        values[i] += value

    frequency = data["freq"]

for i in range(len(values)):
    values[i] /= len(args.files)

result = pd.DataFrame({
    "freq": frequency,
    "magnitude": values
})

result.to_csv(args.output + filename, index=False)
