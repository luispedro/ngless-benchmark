#! /usr/bin/env python3

import os
import re
import shutil
from jug import TaskGenerator, barrier
from glob import glob
import pandas as pd


@TaskGenerator
def run_time(target, ncpu, _):
    import subprocess
    args = ['/usr/bin/time', '--verbose', './run_mocat_{0}.sh'.format(target), str(ncpu)]
    try:
        p = subprocess.run(args,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           check=True)
    except subprocess.CalledProcessError as e:
        print(e.stdout)
        print(e.stderr)
        raise
    else:
        return (p.stdout, p.stderr)


@TaskGenerator
def remove_data_and_results(_):
    for folder in glob("SAMEA*"):
        shutil.rmtree(folder, ignore_errors=True)

    for file in glob("MOCATJob_*"):
        os.remove(file)

    file = "MOCAT.cutoff5prime_calculated"
    if os.path.isfile(file):
        os.remove(file)


@TaskGenerator
def create_data_dirs(target, replicate):
    for folder in glob("../data/{0}/*SAMEA*".format(target)):
        os.mkdir(os.path.basename(folder))
        for file in glob(os.path.join(folder, "*.fq.gz")):

            src = "../{0}".format(file)

            newfile = re.sub(r'(.*)_([0-9])\.(fastq|fq)\.gz', r'\1.\2.fq.gz',
                             os.path.basename(file))
            dst = "{0}/{1}".format(os.path.basename(folder), newfile)

            os.symlink(src, dst)
    return target


@TaskGenerator
def flush_logs():
    if os.path.isdir("logs"):
        shutil.rmtree("logs", ignore_errors=True)

    os.mkdir("logs")


@TaskGenerator
def process_results():
    data = []

    with open("timing-individual") as fh:
        row = {}
        for line in fh:
            if line.strip().startswith("Command exited with non-zero"):
                continue

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


NCPU = 8
NREPLICATES = 3

flush_logs()

outs = {}
for rep in range(NREPLICATES):
    for target in ['gut', 'tara']:
        target = create_data_dirs(target, rep)
        time = run_time(target, NCPU, rep)
        outs[target, rep] = time
        remove_data_and_results(time)
        barrier()

process_results()
