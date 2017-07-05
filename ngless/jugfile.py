from jug import TaskGenerator, barrier

@TaskGenerator
def run_time(script, ncpu, tag):
    '''

    Argument tag is ignored, but is necessary to distinguish the different runs
    of the script.

    '''
    import subprocess
    args = ['/usr/bin/time', '--verbose', 'ngless', '-j', str(ncpu), '--trace', script]
    p = subprocess.run(args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True)
    return (p.stdout, p.stderr)

@TaskGenerator
def cleanup_ngless():
    import shutil
    shutil.rmtree('ngless-locks', ignore_errors=True)
    shutil.rmtree('ngless-partials', ignore_errors=True)
    shutil.rmtree('ngless-stats', ignore_errors=True)

NCPU=8
NREPLICATES=3

outs = {}
for rep in range(NREPLICATES):
    cleanup_ngless()
    for sc in ['ocean.ngl', 'gut.ngl']:
        for i in range(3):
            outs[sc, rep, i] = run_time(sc, NCPU, rep*NREPLICATES + i)
    barrier()

