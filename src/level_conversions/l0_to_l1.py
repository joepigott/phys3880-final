# convert level 0 (raw) data to level 1 (relative) data

import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, required=True)
parser.add_argument("file", nargs=argparse.REMAINDER)
args = parser.parse_args()

if args.output[-1] != "/":
    args.output += "/"

for file in args.file:
    filename = file.split("/")[-1].replace("l0", "l1")

    # read data
    raw = pd.read_csv(file)

    values = raw["value"] - raw["value"].mean()
    dates = raw["created_at"]

    # write data
    final = pd.DataFrame({
        "value": values,
        "created_at": dates
    })

    if "start" in raw.columns:
        final["start"] = raw["start"]
        final["end"] = raw["end"]

    if "hour" in raw.columns:
        final["hour"] = raw["hour"]

    final.to_csv(args.output + filename, index=False)
