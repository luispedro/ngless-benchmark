#! /usr/bin/env python3

import os
import re
import shutil
from jug import TaskGenerator, barrier
from glob import glob


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
    for folder in glob("../data/{0}/SAMEA*".format(target)):
        os.mkdir(os.path.basename(folder))
        for file in glob(os.path.join(folder, "*")):

            src = "../{0}".format(file)

            newfile = re.sub(r'(.*)_([0-9])\.fastq\.gz', r'\1.\2.fq.gz',
                             os.path.basename(file))
            dst = "{0}/{1}".format(os.path.basename(folder), newfile)

            os.symlink(src, dst)
    return target


@TaskGenerator
def flush_logs():
    if os.path.isdir("logs"):
        shutil.rmtree("logs", ignore_errors=True)

    os.mkdir("logs")


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
