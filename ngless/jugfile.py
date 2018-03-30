from jug import TaskGenerator, barrier

@TaskGenerator
def run_time(target, ncpu, _):
    print("RUNNING {}".format(target))
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
def cleanup_ngless(_):
    import shutil
    shutil.rmtree('ngless-locks', ignore_errors=True)
    shutil.rmtree('ngless-partials', ignore_errors=True)
    shutil.rmtree('ngless-stats', ignore_errors=True)
    shutil.rmtree('gut-temp', ignore_errors=True)
    shutil.rmtree('ocean-temp', ignore_errors=True)


@TaskGenerator
def make_temp_directories(_):
    import os
    os.makedirs('gut-temp/screen-igc')
    os.makedirs('gut-temp/filtered-igc')
    for s in os.listdir('../data/gut/'):
        if not s.startswith('SAME'): continue
        os.makedirs(f'gut-temp/rtf-{s}')
        os.makedirs(f'gut-temp/screen-filter-hg19-{s}')

NCPU = 8
NREPLICATES = 3
NSAMPLES = 3

outs = {}
for rep in range(NREPLICATES):
    cleanup_ngless(rep)
    make_temp_directories(rep)
    for target in [ 'gut0-rtf.ngl',
                    'gut1-s.hg19.ngl',
                    'gut2-f.hg19.ngl',
                    'gut3-motus.ngl',
                    'gut4-s.igc.ngl',
                    'gut5-f.igc.ngl',
                    'gut6-p.igc.ngl',
                    'gut-full.ngl',
                        ]:
        for i in range(NSAMPLES):
            outs[target, rep, i] = run_time(target, NCPU, rep*NREPLICATES + i)
    barrier()

