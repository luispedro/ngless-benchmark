#!/usr/bin/env python

import os
import sys
from subprocess import run, PIPE
BASE_URL = "http://vm-lux.embl.de/~kultima/share/"


# Chdir to the location containing this file
os.chdir(os.path.dirname(os.path.realpath(__file__)))


def download_file(url, target):
    import requests
    with open(target, 'wb') as output:
        r = requests.get(url, stream=True)
        for c in r.iter_content(chunk_size=8192 * 1024):
            output.write(c)

data = {
    "ocean": ("MOCAT/v2.0/OM-RGC.zip", "OM-RGC.zip"),
    "igc": ("MOCAT/v2.0/IGC.zip", "IGC.zip"),
    "human": ("MOCAT/data/hg19.gz", "hg19"),
}

print("Downloading MOCAT2")
target = "MOCAT2.zip"
download_file(BASE_URL + "MOCAT/v2.0/MOCAT2.zip", target)
print("Unpacking MOCAT2")
run(["unzip", target], check=True)
os.remove(target)

MOCAT_SRC = "MOCAT/src/"
MOCAT_BIN = "MOCAT/bin/"
MOCAT_DATA = "MOCAT/data/"

mocatpl = MOCAT_SRC + "MOCAT.pl"
if not os.path.isfile(mocatpl):
    print("Failed to find f{mocatpl}. Did something happen to MOCAT2.zip's download?")

prev_dir = os.getcwd()
os.chdir(MOCAT_DATA)

print("Downloading MOCAT data [this can take a while and will take 48GiB of disk space after extraction]...")
for dataset, (url, target) in data.items():
    print(f"Downloading {target}...")
    download_file(BASE_URL + url, target)

    if target.endswith(".zip"):
        run(["unzip", target], check=True)
        os.remove(target)
    elif target.endswith(".tar.gz"):
        run(["tar", "xf", target], check=True)
        os.remove(target)

print("Downloads complete. Preparing databases next")

os.chdir(prev_dir)

os.environ["PERL5LIB"] = ":".join([MOCAT_SRC, os.environ.get("PERL5LIB", '')])
os.environ["PATH"] = ":".join([MOCAT_SRC, MOCAT_BIN, os.environ.get("PATH", '')])

print("Be warned this will take a long time (several hours to days)")
print("Indexing hg19")
run(["MOCAT/bin/2bwt-builder", "MOCAT/data/hg19"], check=True, env=os.environ)

print("Indexing IGC - part 1 of 2")
run(["MOCAT/bin/2bwt-builder", "MOCAT/data/IGC.1"], check=True, env=os.environ)
print("Indexing IGC - part 2 of 2")
run(["MOCAT/bin/2bwt-builder", "MOCAT/data/IGC.2"], check=True, env=os.environ)

print("Indexing OM-RGC - part 1 of 9")
run(["MOCAT/bin/2bwt-builder", "MOCAT/data/OM-RGC.1"], check=True, env=os.environ)
print("Indexing OM-RGC - part 2 of 9")
run(["MOCAT/bin/2bwt-builder", "MOCAT/data/OM-RGC.2"], check=True, env=os.environ)
print("Indexing OM-RGC - part 3 of 9")
run(["MOCAT/bin/2bwt-builder", "MOCAT/data/OM-RGC.3"], check=True, env=os.environ)
print("Indexing OM-RGC - part 4 of 9")
run(["MOCAT/bin/2bwt-builder", "MOCAT/data/OM-RGC.4"], check=True, env=os.environ)
print("Indexing OM-RGC - part 5 of 9")
run(["MOCAT/bin/2bwt-builder", "MOCAT/data/OM-RGC.5"], check=True, env=os.environ)
print("Indexing OM-RGC - part 6 of 9")
run(["MOCAT/bin/2bwt-builder", "MOCAT/data/OM-RGC.6"], check=True, env=os.environ)
print("Indexing OM-RGC - part 7 of 9")
run(["MOCAT/bin/2bwt-builder", "MOCAT/data/OM-RGC.7"], check=True, env=os.environ)
print("Indexing OM-RGC - part 8 of 9")
run(["MOCAT/bin/2bwt-builder", "MOCAT/data/OM-RGC.8"], check=True, env=os.environ)
print("Indexing OM-RGC - part 9 of 9")
run(["MOCAT/bin/2bwt-builder", "MOCAT/data/OM-RGC.9"], check=True, env=os.environ)

print("All done")
