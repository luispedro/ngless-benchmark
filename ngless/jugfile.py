from jug import TaskGenerator, barrier

@TaskGenerator
def run_time(target, ncpu, _):
    print("RUNNING {} on {} CPUS".format(target, ncpu))
    import subprocess
    args = ['/usr/bin/time', '--verbose', 'ngless', '--trace', target, '-j', str(ncpu)]
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
def parse_output(out):
    from parse_time import parse
    return parse(out[1].decode('ascii'))

@TaskGenerator
def cleanup_ngless(_):
    import shutil
    shutil.rmtree('ngless-locks', ignore_errors=True)
    shutil.rmtree('ngless-partials', ignore_errors=True)
    shutil.rmtree('ngless-stats', ignore_errors=True)

@TaskGenerator
def deep_clean(_):
    import shutil
    shutil.rmtree('gut-temp', ignore_errors=True)
    shutil.rmtree('tara-temp', ignore_errors=True)


@TaskGenerator
def make_temp_directories(_):
    import os
    os.makedirs('gut-temp/screen-igc')
    os.makedirs('gut-temp/filtered-igc')
    for s in os.listdir('../data/gut/'):
        if not s.startswith('SAME'): continue
        os.makedirs(f'gut-temp/rtf-{s}')
        os.makedirs(f'gut-temp/screen-filter-hg19-{s}')
    for s in os.listdir('../data/tara/'):
        if not s.startswith('SAME'): continue
        os.makedirs(f'tara-temp/{s}')


@TaskGenerator
def save_to(outs, oname):
    import pandas as pd
    pd.DataFrame(outs).T.to_csv(oname, sep='\t')

@TaskGenerator
def summarize(outs_cpu):
    import numpy as np
    from collections import defaultdict
    total = defaultdict(float)
    for k,v in outs_cpu.items():
        target, rep, i, ncpu = k
        total[target, ncpu] += v['wallclock']
    total = dict(total)

    times = {}
    frac = {}
    for s in set(s for s,_ in total):
        cp = list(set(c for sc,c in total if sc == s))
        cp.sort()
        times[s]  = np.array([total[s, c] for c in cp])
        frac[s] = times[s][0]/times[s]
    return times, frac


NCPU = 8
NREPLICATES = 3
CPU_NREPLICATES = 3
NSAMPLES = 3

outs = {}
outs_cpu = {}
for rep in range(NREPLICATES):
    barrier()
    prev = {'replicate': rep}
    prev = cleanup_ngless(prev)
    prev = deep_clean(prev)
    prev = make_temp_directories(prev)
    for target in [ 'gut0-rtf.ngl',
                    'gut1-s.hg19.ngl',
                    'gut2-f.hg19.ngl',
                    'gut3-motus.ngl',
                    'gut4-s.igc.ngl',
                    'gut5-f.igc.ngl',
                    'gut6-p.igc.ngl',
                    'gut.ngl',

                    'ocean0-rtf.ngl',
                    'ocean1-s-om-rgc.ngl',
                    'ocean2-f-om-rgc.ngl',
                    'ocean3-p-functional-om-rgc.ngl',
                    'ocean4-p-seqname-om-rgc.ngl',
                    'ocean.ngl',
                        ]:
        for i in range(NSAMPLES):
            c = run_time(target, NCPU, prev)
            outs[target, rep, i] = parse_output(c)
            prev = c

save_to(outs, '../data/precomputed/ngless_benchmark.tsv')

for rep in range(CPU_NREPLICATES):
    barrier()
    prev = {'replicate': rep, 'vary-cpu': True}
    for ncpu in [1]: # , 2, 4, 6, 8, 12, 16, 20, 24, 28, 32]:
        cleanup_ngless(prev)
        for target in [ 'gut0-rtf.ngl',
                        'gut1-s.hg19.ngl',
                        'gut2-f.hg19.ngl',
                        'gut4-s.igc.ngl',
                        'gut5-f.igc.ngl',
                        'gut6-p.igc.ngl',
                        'gut.ngl',

                        'ocean0-rtf.ngl',
                        'ocean1-s-om-rgc.ngl',
                        'ocean2-f-om-rgc.ngl',
                        'ocean3-p-functional-om-rgc.ngl',
                        'ocean4-p-seqname-om-rgc.ngl',
                        'ocean.ngl',
                        ]:
            for i in range(NSAMPLES):
                c = run_time(target, ncpu, prev)
                outs_cpu[target, rep, i, ncpu] = parse_output(c)
                prev = c
            prev.hash()

summary = summarize(outs_cpu)
