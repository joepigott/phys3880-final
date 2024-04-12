# given a start and end time, split the dataset into hourly files and save them
# in an output directory named after the duration

import argparse
import pandas as pd

# size of the split files in hours
HOURS = 2

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str, required=True)
parser.add_argument("--start", type=str, required=True)
parser.add_argument("--end", type=str, required=True)
parser.add_argument("--output", type=str, required=True)
args = parser.parse_args()

if args.output[-1] != "/":
    args.output += "/"

raw = pd.read_csv(args.file)
raw = raw[(raw["created_at"] >= args.start) & (raw["created_at"] <= args.end)]

# write entire range to its own file
entire = raw.copy()

filename = args.file.split("/")[-1].split(".")[0]
filename = "_".join(filename.split("_")[:-2] + [args.start, args.end])

# add start and end dates as metadata
start = [f"{args.start}"]
end = [f"{args.end}"]
hour = [""]

for _ in range(len(entire) - 1):
    start.append("")
    end.append("")
    hour.append("")

entire["start"] = start
entire["end"] = end

entire.to_csv(args.output + filename + ".csv", index=False)

# split dataset into bihourly files
for i in range(0, len(raw), HOURS * 60):
    split = raw[i:i+(HOURS * 60)].copy()

    # add start and end dates and hour index as metadata
    start = [f"{args.start}"]
    end = [f"{args.end}"]
    hour = [f"{i // (HOURS * 60)}"]

    for _ in range(len(split) - 1):
        start.append("")
        end.append("")
        hour.append("")

    split["start"] = start
    split["end"] = end
    split["hour"] = hour
    
    split.to_csv(args.output + (filename + f"_{i // (HOURS * 60)}.csv"), index=False)
