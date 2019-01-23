from jug import TaskGenerator

BASEDIR_GUT = '../data/simulated_gut/'
BASEDIR_MARINE = '../data/simulated_tara/'

def run_ngless(sc, idir, odir):
    from jug.utils import jug_execute
    from os import makedirs
    makedirs(odir, exist_ok=True)
    jug_execute.f(['ngless', '--trace', '-j', 'auto', sc, idir, odir])

@TaskGenerator
def run_gut(s):
    run_ngless('human-gut-profiler.ngl', BASEDIR_GUT + s, 'RESULTS_gut/' + s)
@TaskGenerator
def run_marine(s):
    run_ngless('marine-profiler.ngl', BASEDIR_MARINE + s, 'RESULTS_marine/' + s)

for s in open(BASEDIR_GUT + 'simulated_gut'):
    run_gut(s.strip())

for s in open(BASEDIR_MARINE + 'simulated_tara'):
    run_marine(s.strip())
