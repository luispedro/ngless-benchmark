# coding: utf-8
import pandas as pd

data = []

with open("timing-individual") as fh:
    row = {}
    for line in fh:
        name, value = line.strip().split(": ")
        value = value.strip('"')

        if name == "Elapsed (wall clock) time (h:mm:ss or m:ss)":
            if '.' in value:
                value = value.split(":")
                value[-1] = round(float(value[-1]))
            else:
                value = value.split(":")

            if len(value) == 2:
                seconds = int(value[0]) * 60 + int(value[1])
            elif len(value) == 3:
                seconds = int(value[0]) * 3600 + int(value[1]) * 60 + int(value[2])
            else:
                raise Exception("Unknown time format {}".format(value))
            value = seconds

        row[name] = value

        if name == "Exit status":
            data.append(row)
            row = {}

d = pd.DataFrame(data)
d["Command being timed"] = d["Command being timed"].str.replace("MOCAT.pl -cfg MOCAT.cfg -sf ", "")
d["Command being timed"] = d["Command being timed"].str.replace(" -cpus 8", "")
d['dataset'], d["Command being timed"] = d["Command being timed"].str.split(' ', 1).str
d['action'], d["Command being timed"] = d["Command being timed"].str.split(' ', 1).str
d.loc[d["Command being timed"] == "-config", "Command being timed"] = " "
d['target'], d["Command being timed"] = d["Command being timed"].str.split(' ', 1).str

d.loc[d["action"] == "-rtf", "action"] = "ReadTrimFilter"
d.loc[d["action"] == "-s", "action"] = "Screen"
d.loc[d["action"] == "-p", "action"] = "Profile"
d.loc[d["action"] == "-f", "action"] = "Filter"
d.rename({"Elapsed (wall clock) time (h:mm:ss or m:ss)": "Elapsed time"}, axis="columns", inplace=True)

d.to_csv("mocat_benchmark.csv")
