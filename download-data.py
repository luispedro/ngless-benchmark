#!/usr/bin/env python

from os import makedirs, path
ENA_BASE_URL = 'http://ftp.sra.ebi.ac.uk/vol1/fastq/'

def download_file(url, target):
    import requests
    with open(target, 'wb') as output:
        r = requests.get(url, stream=True)
        for c in r.iter_content(chunk_size=8192 * 1024):
            output.write(c)

data = {
    'tara' : {
        'SAMEA2621229' : ['ERR594/ERR594355/ERR594355_1.fastq.gz'],

        'SAMEA2621155' : ['ERR599/ERR599133/ERR599133_1.fastq.gz'],

        'SAMEA2621033' : ['ERR594/ERR594391/ERR594391_1.fastq.gz']
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
                        'ERR478/ERR478967/ERR478967_1.fastq.gz']
        }
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
            download_file(ENA_BASE_URL + f, target)
    with open(path.join('data', benchgroup, benchgroup), 'wt') as slist:
        for sample in entries.keys():
            slist.write(f"{sample}\n")
print("Done.")
