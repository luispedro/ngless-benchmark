#! /usr/bin/env python3

import os
import re
from jug import TaskGenerator, barrier
from glob import glob

samples = {
        'gut': [line.strip() for line in open('../data/gut/gut')],
        'tara': [line.strip() for line in open('../data/tara/tara')],
        }



def run_time(args, stdout=None):
    import subprocess
    args = ['/usr/bin/time', '--verbose'] + args
    try:
        if stdout is None:
            stdout = subprocess.PIPE
        p = subprocess.run(args,
                           stdout=stdout,
                           stderr=subprocess.PIPE,
                           check=True)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise
    else:
        return p.stderr



@TaskGenerator
def run_map(sample, ref, oname, ncpus, _):
    in1,in2 = sorted(glob(sample + '/*.gz'))
    return run_time(['bwa', 'mem', f'-t{ncpus}', f'references/{ref}.fna', in1, in2], stdout=open(oname, 'wb'))


@TaskGenerator
def run_featureCount(samname, ref, oname, ncpu, _):
    return run_time(['featureCounts', '-o', oname,
                '-T1', # Should be f'-T{ncpu}', but featureCounts then crashes
                '-a', f'references/{ref}.gff',
                '-t', 'eggnog45', '-g', 'NOG',
                samname])


@TaskGenerator
def run_htseq_count(samname, ref, oname, _ncpu, _rep):
    with open(oname, 'wb') as out:
        return run_time(['htseq-count',
                    '--quiet',
                    '-f', 'sam',
                    '-s', 'no',
                    '-t', 'eggnog45',
                    '-i', 'NOG',
                    samname,
                    f'references/{ref}.gff'],
                    stdout=out)


@TaskGenerator
def create_data_dirs(samples):
    os.makedirs('data/', exist_ok=True)
    os.makedirs('gut-temp/', exist_ok=True)
    os.makedirs('tara-temp/', exist_ok=True)
    for target in samples:
        for s in samples[target]:
            files = glob(f'../data/{target}/{s}/*.fastq.gz')
            os.makedirs(f'data/{target}/{s}', exist_ok=True)
            if len(files) == 2:
                for f in files:
                    os.symlink('../../../'+f, f'data/{target}/{s}/'+os.path.basename(f))
            else:
                with open(f'data/{target}/{s}/concat.1.fq.gz', 'wb') as out1, \
                     open(f'data/{target}/{s}/concat.2.fq.gz', 'wb') as out2:
                    for f in files:
                        out = (out1 if f.endswith('_1.fastq.gz') else out2)
                        with open(f, 'rb') as ifile:
                            while True:
                                data = ifile.read(8192)
                                if not data:
                                    break
                                out.write(data)


NCPU = 8
NREPLICATES = 3

create_data_dirs(samples)
barrier()
reference = {
        'gut': 'IGC',
        'tara': 'OM-RGC',
        }

outs = {}
prev = None
for rep in range(NREPLICATES):
    for target in ['gut', 'tara']:
        for s in samples[target]:
            samname = f'{target}-temp/{s}.{rep}.mapped.sam'
            oname = f'outputs/{s}.{rep}.txt'
            c = run_map(f'data/{target}/{s}', reference[target], samname, NCPU, rep)
            outs[target, 'map', s, rep] = c
            if target == 'gut':
                outs[target, 'htseq-count', s, rep] = run_htseq_count(samname, reference[target], oname, NCPU, c)
