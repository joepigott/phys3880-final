# l4 data is the l3 data with the average spectrum subtracted (then normalized?)

import argparse
import pandas as pd

argparser = argparse.ArgumentParser()
argparser.add_argument("--output", type=str, required=True)
argparser.add_argument("--average", type=str, required=True)
argparser.add_argument("files", nargs=argparse.REMAINDER)
args = argparser.parse_args()

if args.output[-1] != "/":
    args.output += "/"

average = pd.read_csv(args.average)

av_spectrum = average["magnitude"].values

for file in args.files:
    # dont' do the last one, it will not be of the same length
    if file == args.files[-1]:
        continue

    data = pd.read_csv(file)

    spectrum = data["magnitude"].values
    spectrum -= av_spectrum

    data["magnitude"] = spectrum

    filename = file.split("/")[-1].replace("l2", "l3")
    data.to_csv(args.output + filename, index=False)
