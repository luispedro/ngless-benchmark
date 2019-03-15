#! /usr/bin/env python3

import os
import re
from jug import TaskGenerator, barrier
from glob import glob

NCPUS = 8
samples = {
        'simulated_gut': [line.strip() for line in open('../data/simulated_gut/simulated_gut')],
        'simulated_tara': [line.strip() for line in open('../data/simulated_tara/simulated_tara')],
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
def run_map(sample, ref, oname):
    in1,in2 = sorted(glob(sample + '/*.gz'))
    return run_time(['bwa', 'mem', f'-t{NCPUS}', f'references/{ref}.fna', in1, in2], stdout=open(oname, 'wb'))


@TaskGenerator
def run_htseq_count(samname, ref, oname, _):
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
            files = glob(f'../data/{target}/{s}/*.fq.gz')
            os.makedirs(f'data/{target}/{s}', exist_ok=True)
            if len(files) == 2:
                for f in files:
                    os.symlink('../../../'+f, f'data/{target}/{s}/'+os.path.basename(f))
            else:
                with open(f'data/{target}/{s}/concat.1.fq.gz', 'wb') as out1, \
                     open(f'data/{target}/{s}/concat.2.fq.gz', 'wb') as out2:
                    for f in sorted(files):
                        out = (out1 if f.endswith('_1.fq.gz') else out2)
                        with open(f, 'rb') as ifile:
                            while True:
                                data = ifile.read(8192)
                                if not data:
                                    break
                                out.write(data)



create_data_dirs(samples)
barrier()
reference = {
        'gut': 'IGC',
        'tara': 'OM-RGC',
        }

cs = []
for target in ['gut', 'tara']:
    for s in samples['simulated_'+target]:
        samname = f'{target}-temp/{s}.mapped.sam'
        oname = f'htseq-outputs/{s}.txt'
        c = run_map(f'data/simulated_{target}/{s}', reference[target], samname)
        run_htseq_count(samname, reference[target], oname, c)
        cs.append(c)
