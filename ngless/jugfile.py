from jug import TaskGenerator, barrier

@TaskGenerator
def run_time(script, ncpu):
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
        for _ in range(3):
            outs[sc, rep] = run_time(sc, NCPU)
    barrier()

