#!/usr/bin/env python

import subprocess
from os import makedirs, path
ENA_BASE_URL = 'http://ftp.sra.ebi.ac.uk/vol1/fastq/'
ASPERA_BASE = 'era-fasp@fasp.sra.ebi.ac.uk:vol1/fastq/'
ASPERA_BINARY = path.expanduser('~/.aspera/connect/bin/ascp')
ASPERA_KEY = path.expanduser('~/.aspera/connect/etc/asperaweb_id_dsa.openssh')
ASPERA = path.isfile(ASPERA_BINARY)

def download_file(url, target):
    if ASPERA and not url.startswith("http"):
        cmdline = [
                ASPERA_BINARY,
                '-P33001', # Use special port
                '-T', # No encryption
                '-i', ASPERA_KEY,
                ASPERA_BASE + url,
                target]
        subprocess.run(cmdline, check=True)

    else:
        if not url.startswith("http"):
            url = ENA_BASE_URL + url

        import requests
        with open(target, 'wb') as output:
            r = requests.get(url, stream=True)
            for c in r.iter_content(chunk_size=8192 * 1024):
                output.write(c)

data = {
    'tara' : {
        'SAMEA2621229' : ['ERR594/ERR594355/ERR594355_1.fastq.gz'],
        'SAMEA2621155' : ['ERR599/ERR599133/ERR599133_1.fastq.gz'],
        'SAMEA2621033' : ['ERR594/ERR594391/ERR594391_1.fastq.gz'],
        'SAMEA2622357' : ['ERR594/ERR594357/ERR594357_1.fastq.gz'],
        'SAMEA2621107' : ['ERR275/005/ERR2752145/ERR2752145_1.fastq.gz'],
        'SAMEA2621010' : ['ERR275/006/ERR2752146/ERR2752146_1.fastq.gz',
                          'ERR275/007/ERR2752147/ERR2752147_1.fastq.gz'],
        'SAMEA2621247' : ['ERR275/008/ERR2752148/ERR2752148_1.fastq.gz'],
        'SAMEA2621300' : ['ERR275/009/ERR2752149/ERR2752149_1.fastq.gz',
                          'ERR275/000/ERR2752150/ERR2752150_1.fastq.gz'],
        },
    'gut' : {
        'SAMEA2467039' : ['ERR478/ERR478958/ERR478958_1.fastq.gz',
                          'ERR478/ERR478959/ERR478959_1.fastq.gz',
                          'ERR478/ERR478960/ERR478960_1.fastq.gz',
                          'ERR478/ERR478961/ERR478961_1.fastq.gz'],
        'SAMEA2466896' : ['ERR478/ERR478962/ERR478962_1.fastq.gz',
                          'ERR478/ERR478963/ERR478963_1.fastq.gz'],
        'SAMEA2466965' : ['ERR478/ERR478964/ERR478964_1.fastq.gz',
                          'ERR478/ERR478965/ERR478965_1.fastq.gz',
                          'ERR478/ERR478966/ERR478966_1.fastq.gz',
                          'ERR478/ERR478967/ERR478967_1.fastq.gz'],
        'SAMEA2467015' : ['ERR479/ERR479118/ERR479118_1.fastq.gz',
                          'ERR479/ERR479119/ERR479119_1.fastq.gz',
                          'ERR479/ERR479120/ERR479120_1.fastq.gz',
                          'ERR479/ERR479121/ERR479121_1.fastq.gz'],
        'SAMEA2466953' : ['ERR479/ERR479122/ERR479122_1.fastq.gz',
                          'ERR479/ERR479123/ERR479123_1.fastq.gz'],
        'SAMEA2466996' : ['ERR479/ERR479124/ERR479124_1.fastq.gz',
                          'ERR479/ERR479125/ERR479125_1.fastq.gz',
                          'ERR479/ERR479126/ERR479126_1.fastq.gz',
                          'ERR479/ERR479127/ERR479127_1.fastq.gz'],
        'SAMEA2466952' : ['ERR479/ERR479136/ERR479136_1.fastq.gz',
                          'ERR479/ERR479137/ERR479137_1.fastq.gz'],
        'SAMEA2466916' : ['ERR479/ERR479140/ERR479140_1.fastq.gz',
                          'ERR479/ERR479141/ERR479141_1.fastq.gz'],
        },
    'simulated_tara' : {
        'from_SAMEA2621229' : ['https://zenodo.org/record/2539432/files/from_SAMEA2621229_1.fastq.gz'],
        'from_SAMEA2621155' : ['https://zenodo.org/record/2539432/files/from_SAMEA2621155_1.fastq.gz'],
        'from_SAMEA2621033' : ['https://zenodo.org/record/2539432/files/from_SAMEA2621033_1.fastq.gz'],
        'from_SAMEA2622357' : ['https://zenodo.org/record/2539432/files/from_SAMEA2622357_1.fastq.gz'],
        'from_SAMEA2621107' : ['https://zenodo.org/record/2539432/files/from_SAMEA2621107_1.fastq.gz'],
        'from_SAMEA2621010' : ['https://zenodo.org/record/2539432/files/from_SAMEA2621010_1.fastq.gz'],
        'from_SAMEA2621247' : ['https://zenodo.org/record/2539432/files/from_SAMEA2621247_1.fastq.gz'],
        'from_SAMEA2621300' : ['https://zenodo.org/record/2539432/files/from_SAMEA2621300_1.fastq.gz'],
        },
    'simulated_gut' : {
        'from_SAMEA2467039' : ['https://zenodo.org/record/2539432/files/from_SAMEA2467039_1.fastq.gz'],
        'from_SAMEA2466896' : ['https://zenodo.org/record/2539432/files/from_SAMEA2466896_1.fastq.gz'],
        'from_SAMEA2466965' : ['https://zenodo.org/record/2539432/files/from_SAMEA2466965_1.fastq.gz'],
        'from_SAMEA2467015' : ['https://zenodo.org/record/2539432/files/from_SAMEA2467015_1.fastq.gz'],
        'from_SAMEA2466953' : ['https://zenodo.org/record/2539432/files/from_SAMEA2466953_1.fastq.gz'],
        'from_SAMEA2466996' : ['https://zenodo.org/record/2539432/files/from_SAMEA2466996_1.fastq.gz'],
        'from_SAMEA2466952' : ['https://zenodo.org/record/2539432/files/from_SAMEA2466952_1.fastq.gz'],
        'from_SAMEA2466916' : ['https://zenodo.org/record/2539432/files/from_SAMEA2466916_1.fastq.gz'],
        },
    }

print("Downloading data [this can take a while and will take ca. 50GiB of disk space]...")
for benchgroup, entries in data.items():
    for sample, fqs in entries.items():
        basedir = path.join('data', benchgroup, sample)
        makedirs(basedir, exist_ok=True)
        fqs += [f.replace('_1.fastq', '_2.fastq') for f in fqs]
        for f in fqs:
            target = path.join(basedir, path.basename(f))
            print(f"Downloading {target}...")
            download_file(f, target)
    with open(path.join('data', benchgroup, benchgroup), 'wt') as slist:
        for sample in entries.keys():
            slist.write(f"{sample}\n")
print("Done.")
