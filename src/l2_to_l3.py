# level 3 data is normalized level 2 data. l3a is from l2a and l3b is from l2b

import argparse
import pandas as pd
import numpy as np

argparser = argparse.ArgumentParser()
argparser.add_argument("--output", type=str, required=True)
argparser.add_argument("files", nargs=argparse.REMAINDER)
args = argparser.parse_args()

if args.output[-1] != "/":
    args.output += "/"

for file in args.files:
    raw = pd.read_csv(file)

    # normalize
    maximum = np.max(raw["magnitude"])
    raw["magnitude"] = raw["magnitude"] / maximum

    filename = file.split("/")[-1].replace("l2", "l3")

    raw.to_csv(args.output + filename, index=False)
